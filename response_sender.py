"""
Módulo de Envio de Respostas

Este módulo é responsável por enviar as respostas obtidas do ChatGPT para o usuário,
seja por email ou diretamente no chat, conforme a preferência configurada.
"""

import smtplib
import os
from dotenv import load_dotenv
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class ResponseSender:
    """
    Classe responsável pelo envio das respostas ao usuário.
    """
    
    def __init__(self, email_destino=None, webhook_url=None):
        """
        Inicializa o enviador de respostas.
        
        Args:
            email_destino (str, optional): Email de destino para envio da resposta
            webhook_url (str, optional): URL do webhook para envio da resposta ao chat
        """
        self.email_destino = email_destino
        self.webhook_url = webhook_url

        load_dotenv()

        # Configurações de email (devem ser ajustadas pelo usuário)
        self.smtp_config = {
            "servidor": "smtp.gmail.com",
            "porta": 587,
            "usuario": os.getenv("EMAIL"),  # Preencher com o email do remetente
            "senha": os.getenv("PASSWORD_SMTP")    # Preencher com a senha de app
        }
    
    def enviar_por_email(self, assunto, conteudo, anexos=None):
        """
        Envia a resposta por email.
        
        Args:
            assunto (str): Assunto do email
            conteudo (str): Conteúdo do email
            anexos (list, optional): Lista de caminhos para arquivos a serem anexados
            
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrário
            str: Mensagem de sucesso ou erro
        """
        if not self.email_destino:
            return False, "Email de destino não configurado."
        
        if not self.smtp_config["usuario"] or not self.smtp_config["senha"]:
            return False, "Configurações de SMTP incompletas."
        
        try:
            # Criação da mensagem
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config["usuario"]
            msg['To'] = self.email_destino
            msg['Subject'] = assunto
            
            # Adicionando o corpo do email
            msg.attach(MIMEText(conteudo, 'plain'))
            
            # Adicionando anexos, se houver
            if anexos:
                for anexo in anexos:
                    if os.path.exists(anexo):
                        with open(anexo, 'rb') as f:
                            # Determina o tipo de anexo
                            if anexo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                # Anexo de imagem
                                img = MIMEImage(f.read())
                                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(anexo))
                                msg.attach(img)
                            else:
                                # Outros tipos de anexo
                                part = MIMEText(f.read().decode('utf-8'), 'plain')
                                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(anexo))
                                msg.attach(part)
            
            # Enviando o email
            with smtplib.SMTP(self.smtp_config["servidor"], self.smtp_config["porta"]) as servidor:
                servidor.starttls()
                servidor.login(self.smtp_config["usuario"], self.smtp_config["senha"])
                servidor.send_message(msg)
            
            return True, f"Email enviado com sucesso para {self.email_destino}"
        except Exception as e:
            return False, f"Erro ao enviar email: {e}"
    
    def enviar_para_chat(self, conteudo, titulo=None):
        """
        Envia a resposta diretamente para o chat usando um webhook.
        
        Args:
            conteudo (str): Conteúdo da resposta
            titulo (str, optional): Título da resposta
            
        Returns:
            bool: True se a resposta foi enviada com sucesso, False caso contrário
            str: Mensagem de sucesso ou erro
        """
        if not self.webhook_url:
            return False, "URL do webhook não configurada."
        
        try:
            # Preparando o payload
            payload = {
                "content": conteudo
            }
            
            if titulo:
                payload["title"] = titulo
            
            # Enviando para o webhook
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201, 204]:
                return True, "Resposta enviada com sucesso para o chat"
            else:
                return False, f"Erro ao enviar para o chat: {response.status_code} - {response.text}"
        except Exception as e:
            return False, f"Erro ao enviar para o chat: {e}"
    
    def salvar_resposta_local(self, conteudo, caminho="resposta_chatgpt.txt"):
        """
        Salva a resposta em um arquivo local.
        
        Args:
            conteudo (str): Conteúdo da resposta
            caminho (str, optional): Caminho do arquivo para salvar a resposta
            
        Returns:
            bool: True se o arquivo foi salvo com sucesso, False caso contrário
            str: Mensagem de sucesso ou erro
        """
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return True, f"Resposta salva com sucesso em {caminho}"
        except Exception as e:
            return False, f"Erro ao salvar resposta: {e}"

# Exemplo de uso:
"""
# Inicializa o enviador de respostas
sender = ResponseSender(email_destino="pog@cin.ufpe.br")

# Envia por email
success, message = sender.enviar_por_email(
    "Solução da Questão de Programação",
    "Aqui está a solução para sua questão de programação...",
    ["captura_tela.png"]
)
print(message)

# Salva localmente
success, message = sender.salvar_resposta_local("Conteúdo da resposta...")
print(message)
"""
