# Script de Automação de Deploy - Agente Gemini (Windows PowerShell)

Write-Host "--- Iniciando Deploy Automático no Google Cloud Run ---" -ForegroundColor Cyan

# Verifica gcloud
if (-not (Get-Command "gcloud" -ErrorAction SilentlyContinue)) {
    Write-Error "Erro: 'gcloud' não encontrado. Certifique-se de ter o Google Cloud CLI instalado e no seu PATH."
    exit 1
}

# Verifica service_account.json
if (-not (Test-Path "service_account.json")) {
    Write-Error "Erro: Arquivo 'service_account.json' não encontrado no diretório atual.`nPor favor, coloque o arquivo de credenciais do Google na mesma pasta deste script."
    exit 1
}

# Configuração do Projeto
$defaultProjectID = "agente-sheets-480715"
$projectID = Read-Host "Por favor, digite o ID do seu Projeto no Google Cloud (Enter para '$defaultProjectID')"
if ([string]::IsNullOrWhiteSpace($projectID)) {
    $projectID = $defaultProjectID
}
if ([string]::IsNullOrWhiteSpace($projectID)) {
    Write-Error "ID do projeto não pode ser vazio."
    exit 1
}

Write-Host "Configurando projeto: $projectID..." -ForegroundColor Yellow
gcloud config set project $projectID

Write-Host "Ativando serviços necessários (Cloud Run, Artifact Registry)..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# Variáveis de Ambiente
Write-Host "--- Configuração de Variáveis de Ambiente ---" -ForegroundColor Cyan
$geminiKey = Read-Host "Cole sua GEMINI_API_KEY" -AsSecureString
$geminiKeyPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($geminiKey))

$spreadsheetID = Read-Host "Cole seu SPREADSHEET_ID"
if ([string]::IsNullOrWhiteSpace($geminiKeyPlain) -or [string]::IsNullOrWhiteSpace($spreadsheetID)) {
    Write-Error "Erro: Chaves não podem ser vazias."
    exit 1
}

Write-Host "Iniciando Deploy... (Isso pode levar alguns minutos)" -ForegroundColor Green

# Executa o deploy
# Nota: Usamos --source . que fará o upload do código para o Cloud Build
gcloud run deploy agente-cadastro `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --set-env-vars "GEMINI_API_KEY=$geminiKeyPlain", "SPREADSHEET_ID=$spreadsheetID"

Write-Host "--- DEPLOY CONCLUÍDO! ---" -ForegroundColor Cyan
Write-Host "Se tudo deu certo, a URL do seu agente está logo acima." -ForegroundColor Green
