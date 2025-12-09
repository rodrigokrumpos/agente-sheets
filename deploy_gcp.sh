#!/bin/bash

# Script de Automação de Deploy - Agente Gemini
# Uso: ./deploy_gcp.sh

echo "--- Iniciando Deploy Automático no Google Cloud Run ---"

# Verifica se está no Cloud Shell ou se tem gcloud
if ! command -v gcloud &> /dev/null; then
    echo "Erro: 'gcloud' não encontrado. Certifique-se de ter o Google Cloud CLI instalado e no seu PATH."
    exit 1
fi

if [ ! -f "service_account.json" ]; then
    echo "Erro: Arquivo 'service_account.json' não encontrado no diretório atual."
    echo "Por favor, coloque o arquivo de credenciais do Google na mesma pasta deste script."
    exit 1
fi

echo "Por favor, digite o ID do seu Projeto no Google Cloud (Project ID):"
read PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "ID do projeto não pode ser vazio."
    exit 1
fi

echo "Configurando projeto: $PROJECT_ID..."
gcloud config set project $PROJECT_ID

echo "Ativando serviços necessários (Cloud Run, Artifact Registry)..."
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

echo "--- Configuração de Variáveis de Ambiente ---"
echo "Cole sua GEMINI_API_KEY (pressione Enter após colar):"
read -s GEMINI_KEY
echo "Cole seu SPREADSHEET_ID (pressione Enter após colar):"
read SPREADSHEET_ID

if [ -z "$GEMINI_KEY" ] || [ -z "$SPREADSHEET_ID" ]; then
    echo "Erro: Chaves não podem ser vazias."
    exit 1
fi

echo "Iniciando Deploy... (Isso pode levar alguns minutos)"

gcloud run deploy agente-cadastro \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="$GEMINI_KEY",SPREADSHEET_ID="$SPREADSHEET_ID"

echo "--- DEPLOY CONCLUÍDO! ---"
echo "Se tudo deu certo, a URL do seu agente está logo acima."
