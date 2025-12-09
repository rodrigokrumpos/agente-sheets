import streamlit as st
from PIL import Image
import pandas as pd
import time
import importlib
import sheets_handler
importlib.reload(sheets_handler)
from sheets_handler import append_to_sheet
from processor import extract_info_from_image

# Configuração da Página
st.set_page_config(
    page_title="Agente de Cadastro",
    page_icon="🤖",
    layout="centered"
)

# Título e Descrição
st.title("🤖 Agente de Cadastro Inteligente v1.1")
st.markdown("""
Faça upload de uma imagem (print, foto, documento) contendo os dados do cliente.
A IA irá extrair **Nome**, **WhatsApp** e **Empreendimento** e salvar na sua planilha.
""")

# Upload de Arquivo
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    # Mostra a imagem carregada
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem Carregada', use_column_width=True)
    
    # Botão para processar
    if st.button('🔍 Processar Imagem', type="primary"):
        with st.spinner('Analisando imagem com IA...'):
            try:
                # Rebobina o arquivo para leitura se necessário
                uploaded_file.seek(0)
                
                # Chama o processador
                data = extract_info_from_image(uploaded_file)
                
                st.success("Dados extraídos com sucesso!")
                
                # Mostra os dados em formato de Cartão/Tabela
                col1, col2, col3 = st.columns(3)
                col1.metric("Nome", data.get("nome") or "Não encontrado")
                col2.metric("WhatsApp", data.get("whatsapp") or "Não encontrado")
                col3.metric("Empreendimento", data.get("empreendimento") or "Não encontrado")
                
                # Salva no Sheets
                with st.status("Salvando no Google Sheets...", expanded=True) as status:
                    st.write("Conectando à planilha...")
                    append_to_sheet(data)
                    status.update(label="Salvo com sucesso!", state="complete", expanded=False)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"Ocorreu um erro durante o processamento: {e}")
