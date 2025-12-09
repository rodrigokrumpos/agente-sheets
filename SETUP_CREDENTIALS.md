# Guia de Configuração de Credenciais

Para que este agente funcione, você precisa de duas coisas:

## 1. API Key do Gemini (Google AI)
1. Acesse [Google AI Studio](https://aistudio.google.com/).
2. Crie uma API Key.
3. Cole a chave no arquivo `.env` na variável `GEMINI_API_KEY`.

## 2. Google Sheets API (Service Account)
1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto.
3. Vá em **APIs & Services > Library** e ative as seguintes APIs:
    - **Google Sheets API**
    - **Google Drive API**
4. Vá em **APIs & Services > Credentials**.
5. Clique em **Create Credentials > Service Account**.
6. Dê um nome e crie.
7. Clique na Service Account criada, vá na aba **Keys** > **Add Key** > **Create new key** > **JSON**.
8. Um arquivo será baixado. Renomeie-o para `service_account.json` e coloque na pasta `gemini-sheet-agent`.
9.*. **IMPORTANTE**: Abra o arquivo `service_account.json`, copie o email (`client_email`) e compartilhe sua planilha do Google Sheets (`https://docs.google.com/spreadsheets/d/1uVuQ3M8N_9O0EqixdGdRJHq5l57bVby340jvOuqbAKA/edit`) com esse email, dando permissão de **Editor*
