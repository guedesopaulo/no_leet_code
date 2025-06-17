"""
Programa de Captura de Tela Discreta

Este programa captura a tela inteira do Windows quando uma tecla de atalho é pressionada,
envia a imagem para o ChatGPT para análise de questões de programação,
e retorna a resposta diretamente no ChatGPT ou por email.

O programa funciona de forma discreta, sem ser detectável durante compartilhamento de tela.
"""

import os
import sys
import base64
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import json
import requests
from io import BytesIO
from PIL import ImageGrab
import keyboard
import win32gui
import win32con
import win32process

# Configurações
EMAIL_DESTINO = "pog@cin.ufpe.br"
TECLA_ATALHO = "ctrl+shift+p"  # Tecla de atalho para capturar a tela
OPENAI_API_KEY = ""  # Insira sua chave API aqui

# Variáveis globais
captura_ativa = False
janela_oculta = None

def ocultar_janela():
    """Oculta a janela do console para tornar o programa invisível."""
    janela = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(janela, win32con.SW_HIDE)
    return janela

def mostrar_janela(janela):
    """Mostra a janela do console novamente."""
    if janela:
        win32gui.ShowWindow(janela, win32con.SW_SHOW)

def capturar_tela():
    """Captura a tela inteira e retorna a imagem em formato PIL."""
    try:
        imagem = ImageGrab.grab()
        return imagem
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        return None

def converter_imagem_para_base64(imagem):
    """Converte uma imagem PIL para string base64."""
    buffer = BytesIO()
    imagem.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def enviar_para_chatgpt(imagem_base64):
    """Envia a imagem para o ChatGPT e retorna a resposta."""
    if not OPENAI_API_KEY:
        return "Erro: Chave API do OpenAI não configurada."
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Esta é uma questão de programação que preciso resolver. Por favor, analise a imagem e forneça a solução completa com explicações detalhadas."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{imagem_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Erro na API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erro ao enviar para ChatGPT: {e}"

def enviar_email(conteudo):
    """Envia um email com a resposta do ChatGPT."""
    try:
        # Configuração do servidor SMTP (exemplo para Gmail)
        # Nota: Para uso real, é necessário configurar um servidor SMTP ou usar um serviço de email
        servidor_smtp = "smtp.gmail.com"
        porta = 587
        usuario = "seu_email@gmail.com"  # Substitua pelo seu email
        senha = "sua_senha_app"  # Substitua pela sua senha de app
        
        # Criação da mensagem
        msg = MIMEMultipart()
        msg['From'] = usuario
        msg['To'] = EMAIL_DESTINO
        msg['Subject'] = "Resposta da Questão de Programação"
        
        # Adicionando o corpo do email
        msg.attach(MIMEText(conteudo, 'plain'))
        
        # Enviando o email
        with smtplib.SMTP(servidor_smtp, porta) as servidor:
            servidor.starttls()
            servidor.login(usuario, senha)
            servidor.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def processar_captura():
    """Processa a captura de tela e envia para análise."""
    global captura_ativa
    
    if captura_ativa:
        return
    
    captura_ativa = True
    
    try:
        # Captura a tela
        imagem = capturar_tela()
        if imagem:
            # Converte para base64
            imagem_base64 = converter_imagem_para_base64(imagem)
            
            # Envia para o ChatGPT
            resposta = enviar_para_chatgpt(imagem_base64)
            
            # Salva a resposta em um arquivo temporário
            with open("resposta_chatgpt.txt", "w", encoding="utf-8") as f:
                f.write(resposta)
            
            # Opcionalmente envia por email
            enviar_email(resposta)
            
            print("\nCaptura processada com sucesso!")
            print("A resposta foi salva em 'resposta_chatgpt.txt'")
            if EMAIL_DESTINO:
                print(f"Um email foi enviado para {EMAIL_DESTINO}")
    except Exception as e:
        print(f"Erro ao processar captura: {e}")
    
    captura_ativa = False

def on_hotkey():
    """Função chamada quando a tecla de atalho é pressionada."""
    # Inicia o processamento em uma thread separada para não bloquear
    threading.Thread(target=processar_captura).start()

def main():
    """Função principal do programa."""
    global janela_oculta
    
    print("Programa de Captura de Tela Iniciado")
    print(f"Pressione '{TECLA_ATALHO}' para capturar a tela")
    print("O programa será ocultado em 3 segundos...")
    
    # Aguarda 3 segundos antes de ocultar
    time.sleep(3)
    
    # Oculta a janela do console
    janela_oculta = ocultar_janela()
    
    # Registra a tecla de atalho
    keyboard.add_hotkey(TECLA_ATALHO, on_hotkey)
    
    try:
        # Mantém o programa em execução
        keyboard.wait()
    except KeyboardInterrupt:
        pass
    finally:
        # Mostra a janela novamente ao encerrar
        mostrar_janela(janela_oculta)

if __name__ == "__main__":
    # Verifica se a chave API foi configurada
    if not OPENAI_API_KEY:
        print("AVISO: Você precisa configurar sua chave API do OpenAI no código.")
        print("Edite a variável OPENAI_API_KEY no início do arquivo.")
    
    main()
