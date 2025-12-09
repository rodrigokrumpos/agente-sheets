# Agente Gemini -> Google Sheets

Este agente lê uma imagem, usa inteligência artificial (Gemini) para identificar dados de clientes e salva automaticamente em uma planilha do Google Sheets.

## Instalação

1.  **Pré-requisitos**: Python instalado.
2.  **Instalar dependências**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar Credenciais**:
    - Siga as instruções em `SETUP_CREDENTIALS.md` para obter sua API Key do Gemini e o arquivo `service_account.json` do Google Cloud.
    - Renomeie `.env.example` para `.env` e adicione sua `GEMINI_API_KEY`.
    - Coloque o arquivo `service_account.json` na raiz deste diretório.

## Uso

Execute o script passando o caminho da imagem que deseja processar:

```bash
python main.py caminho/para/sua/imagem.jpg
```

O script irá:
1.  Ler a imagem.
2.  Extrair Nome, WhatsApp e Empreendimento.
3.  Adicionar uma nova linha na planilha configurada.
