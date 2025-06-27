
# FM Global Document Query API

Questo progetto fornisce una semplice API REST per interrogare semanticamente un insieme di documenti PDF (FM Global) e ottenere risposte basate sui contenuti.

## Struttura del progetto
- main.py: Applicazione FastAPI principale
- requirements.txt: Dipendenze Python
- openapi.yaml: Specifica OpenAPI per GPT
- README.md: Istruzioni

## Deploy su Render
1. Crea un nuovo Web Service collegato al repo GitHub
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Aggiungi `OPENAI_API_KEY` come variabile d'ambiente
5. Cartella `pdfs` da creare e riempire con i tuoi documenti

## Endpoint
POST /query
{
  "question": "La tua domanda qui"
}
