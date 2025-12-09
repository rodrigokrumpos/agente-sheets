import os
import logging
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_sheets():
    """Autentica e conecta ao Google Sheets."""
    load_dotenv()
    
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    # Tenta usar st.secrets (Streamlit Cloud)
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            logging.info("Usando credenciais do Streamlit Secrets.")
            creds_dict = dict(st.secrets["gcp_service_account"])
            # Se a private_key tiver quebras de linha escapadas, conserte
             if "private_key" in creds_dict:
                  # Normaliza a chave privada (converte \\n e \\\\n para \n real)
                  creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n").replace("\\n", "\n")
            
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            return client
    except ImportError:
        pass
    except Exception as e:
        logging.warning(f"Erro ao tentar usar secrets do Streamlit: {e}")

    # Fallback para arquivo local (Desenvolvimento Local)
    creds_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "service_account.json")
    
    if not os.path.exists(creds_file):
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {creds_file} e nenhum segredo configurado no Streamlit.")
        
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)
    return client

def get_next_record_id(sheet):
    """Lê a coluna C (recordId) para determinar o próximo ID."""
    try:
        # Pega todos os valores da coluna 3 (C)
        # O resultado vem como uma lista de strings. A primeira linha pode ser o cabeçalho.
        col_values = sheet.col_values(3)
        
        if not col_values:
            return 1
            
        # Filtra apenas números inteiros
        ids = []
        for value in col_values:
            if value.isdigit():
                ids.append(int(value))
        
        if not ids:
            return 1
            
        return max(ids) + 1
    except Exception as e:
        logging.warning(f"Não foi possível calcular recordId, usando 0. Erro: {e}")
        return 0

def append_to_sheet(data, spreadsheet_id=None):
    """
    Adiciona uma nova linha na planilha especificada com mapeamento corrigido.
    Colunas:
    A: Date/Time
    B: Empreendimento
    C: recordId
    D: Email (vazio)
    E: Nome
    F: CPF (vazio)
    G: WhatsApp
    """
    load_dotenv()
    sheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
    
    if not sheet_id:
         raise ValueError("SPREADSHEET_ID não definido.")

    try:
        client = connect_to_sheets()
        # Abre a planilha pelo ID
        sheet = client.open_by_key(sheet_id).sheet1 # Assume que é a primeira aba
        
        # Gera campos automáticos
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        record_id = get_next_record_id(sheet)
        
        # Mapeamento dos dados para as colunas A-G
        # A: Date, B: Empreendimento, C: ID, D: Email, E: Nome, F: CPF, G: Zap
        row = [
            current_time,                       # A: Carimbo de data/hora
            data.get('empreendimento', ''),     # B: Empreendimento
            record_id,                          # C: recordId
            "",                                 # D: Endereço de e-mail (Vazio)
            data.get('nome', ''),               # E: Qual o seu nome completo?
            "",                                 # F: Qual o número do seu CPF? (Vazio)
            data.get('whatsapp', '')            # G: Qual o seu Celular?
        ]
        
        logging.info(f"Adicionando registro (ID: {record_id}): {row}")
        sheet.append_row(row)
        logging.info("Registro adicionado com sucesso ao Google Sheets.")
        
    except Exception as e:
        logging.error(f"Erro ao salvar no Google Sheets: {e}")
        raise
