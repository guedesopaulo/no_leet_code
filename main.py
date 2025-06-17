import threading
import time
from PIL import ImageGrab
import keyboard
import win32gui
import win32con
import os
from dotenv import load_dotenv

# Importando os módulos personalizados
from chatgpt_integration import ChatGPTIntegration
from response_sender import ResponseSender

load_dotenv()

# Configurações
CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "EMAIL_DESTINO": os.getenv("EMAIL"),
    "TECLA_ATALHO": "ctrl+shift+l",  # Tecla de atalho para capturar a tela
    "SALVAR_LOCALMENTE": True,
    "ENVIAR_EMAIL": True,
    "ARQUIVO_RESPOSTA": "resposta_chatgpt.txt"
}

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

def processar_captura():
    """Processa a captura de tela e envia para análise."""
    global captura_ativa
    
    if captura_ativa:
        return
    
    captura_ativa = True
    
    try:
        # Captura a tela
        imagem = ImageGrab.grab()
        
        if imagem:
            # Inicializa a integração com o ChatGPT
            chatgpt = ChatGPTIntegration(CONFIG["OPENAI_API_KEY"])
            
            # Envia a imagem para análise
            _, resposta = chatgpt.analyze_programming_question(imagem)
            
            # Inicializa o enviador de respostas
            sender = ResponseSender(email_destino=CONFIG["EMAIL_DESTINO"])
            
            # Salva a resposta localmente
            if CONFIG["SALVAR_LOCALMENTE"]:
                sucesso, mensagem = sender.salvar_resposta_local(resposta, CONFIG["ARQUIVO_RESPOSTA"])
                print(mensagem)
            
            # Envia por email
            if CONFIG["ENVIAR_EMAIL"] and CONFIG["EMAIL_DESTINO"]:
                sucesso, mensagem = sender.enviar_por_email(
                    "Solução da Questão de Programação",
                    resposta
                )
                print(mensagem)
            
            print("\nCaptura processada com sucesso!")
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
    print(f"Pressione '{CONFIG['TECLA_ATALHO']}' para capturar a tela")
    print("O programa será ocultado em 3 segundos...")
    
    # Aguarda 3 segundos antes de ocultar
    time.sleep(3)
    
    # Oculta a janela do console
    janela_oculta = ocultar_janela()
    
    # Registra a tecla de atalho
    keyboard.add_hotkey(CONFIG["TECLA_ATALHO"], on_hotkey)
    
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
    if not CONFIG["OPENAI_API_KEY"]:
        print("AVISO: Você precisa configurar sua chave API do OpenAI no código.")
        print("Edite a variável OPENAI_API_KEY no dicionário CONFIG no início do arquivo.")
    
    main()
