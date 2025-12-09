import sys
import argparse
import logging
from processor import extract_info_from_image
from sheets_handler import append_to_sheet

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Agente Gemini para extração de dados de imagem para Google Sheets.")
    parser.add_argument("image_path", help="Caminho para o arquivo de imagem.")
    args = parser.parse_args()
    
    image_path = args.image_path
    
    print("--- Agente Gemini Iniciado ---")
    
    try:
        # 1. Extração
        print(f"Lendo imagem: {image_path}...")
        data = extract_info_from_image(image_path)
        print("Dados extraídos:")
        print(f"Nome: {data.get('nome')}")
        print(f"WhatsApp: {data.get('whatsapp')}")
        print(f"Empreendimento: {data.get('empreendimento')}")
        
        # Confirmação simples (opcional em automação total, mas bom para CLI interativa)
        # Em um agente autônomo, poderíamos pular isso, mas vamos manter direto.
        
        # 2. Gravação
        print("Enviando para o Google Sheets...")
        append_to_sheet(data)
        print("--- Sucesso! ---")
        
    except Exception as e:
        print(f"--- Erro Fatal ---")
        logging.error(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
