import requests
import base64
from io import BytesIO
from PIL import Image

class ChatGPTIntegration:
    """
    Classe responsável pela integração com a API do ChatGPT para análise de imagens.
    """
    
    def __init__(self, api_key):
        """
        Inicializa a integração com a API do ChatGPT.
        
        Args:
            api_key (str): Chave de API do OpenAI
        """
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def encode_image(self, image):
        """
        Converte uma imagem PIL para string base64.
        
        Args:
            image (PIL.Image): Imagem a ser codificada
            
        Returns:
            str: String base64 da imagem
        """
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def analyze_programming_question(self, image, custom_prompt=None):
        """
        Envia uma imagem para análise pelo ChatGPT e retorna a solução da questão de programação.
        
        Args:
            image (PIL.Image): Imagem contendo a questão de programação
            custom_prompt (str, optional): Prompt personalizado para enviar junto com a imagem
            
        Returns:
            dict: Resposta completa da API
            str: Texto da solução da questão
        """
        if not self.api_key:
            return None, "Erro: Chave API do OpenAI não configurada."
        
        # Codifica a imagem em base64
        image_base64 = self.encode_image(image)
        
        # Define o prompt padrão se nenhum personalizado for fornecido
        prompt = custom_prompt or "Esta é uma questão de programação que preciso resolver. Por favor, analise a imagem e forneça a solução apenas com código e comentário. Primeiro uma solução mais simples com dicionários (se fizer sentido) e depois uma mais robusta. Em inglês"
        
        # Monta o payload da requisição
        payload = {
            "model": "gpt-4o-mini-2024-07-18",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
        }
        
        try:
            # Envia a requisição para a API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                response_data = response.json()
                solution_text = response_data["choices"][0]["message"]["content"]
                return response_data, solution_text
            else:
                error_message = f"Erro na API: {response.status_code} - {response.text}"
                return None, error_message
                
        except Exception as e:
            error_message = f"Erro ao enviar para ChatGPT: {e}"
            return None, error_message
    
    def save_response(self, response_text, filename="resposta_chatgpt.txt"):
        """
        Salva a resposta do ChatGPT em um arquivo.
        
        Args:
            response_text (str): Texto da resposta
            filename (str, optional): Nome do arquivo para salvar a resposta
            
        Returns:
            bool: True se o arquivo foi salvo com sucesso, False caso contrário
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response_text)
            return True
        except Exception as e:
            print(f"Erro ao salvar resposta: {e}")
            return False

# Exemplo de uso:
"""
# Inicializa a integração
api_key = "sua_chave_api_aqui"
chatgpt = ChatGPTIntegration(api_key)

# Captura a tela
from PIL import ImageGrab
image = ImageGrab.grab()

# Envia para análise
_, solution = chatgpt.analyze_programming_question(image)

# Salva a resposta
chatgpt.save_response(solution)
"""
