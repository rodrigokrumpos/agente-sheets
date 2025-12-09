import os
import json
import logging
import time
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_gemini():
    """Carrega variáveis de ambiente e configura a API do Gemini."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")
    genai.configure(api_key=api_key)

def extract_info_from_image(image_input):
    """
    Envia uma imagem para o Gemini e extrai nome, telefone e empreendimento.
    image_input: Pode ser um caminho de arquivo (str) ou um arquivo/stream aberto.
    Retorna um dicionário com os dados.
    """
    configure_gemini()
    
    # Se for string (caminho), verifica se existe e abre.
    # Se não for string, assume que é um objeto de arquivo (ou bytes) já aberto.
    if isinstance(image_input, str):
        if not os.path.exists(image_input):
            raise FileNotFoundError(f"Imagem não encontrada: {image_input}")
        logging.info(f"Processando imagem: {image_input}")
        img = Image.open(image_input)
    else:
        logging.info("Processando imagem carregada via upload...")
        img = Image.open(image_input)

    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = """
        Analise esta imagem e extraia as seguintes informações se estiverem visíveis:
        1. Nome completo da pessoa (Nome).
        2. Número de telefone (Whatsapp/Celular). Formate apenas com números.
        3. Nome do empreendimento ou interesse (Empreendimento).

        Retorne APENAS um objeto JSON válido com as seguintes chaves: "nome", "whatsapp", "empreendimento".
        Se alguma informação não estiver clara, retorne null para aquele campo.
        Não use markdown, não use blocos de código ```json ```, retorne apenas a string JSON pura.
        """
        
        response = model.generate_content([prompt, img])
        
        # Tratamento básico da resposta para garantir JSON limpo
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        data = json.loads(response_text)
        logging.info("Informações extraídas com sucesso.")
        return data

    except Exception as e:
        logging.error(f"Erro ao processar imagem: {e}")
        raise
