# azure-role-based-assistant
Backend implementation for a simple AI assistant using Azure OpenAI, Azure AI Search, and FastAPI.

This project demonstrates how to create an intelligent assistant, that responds to questions based on their role (e.g. HR, IT). It utilizes retrieval-augmented generation (RAG) technique to provide accurate answers from internal data.

## Setup instructions
1. Clone repository:
```bash
git clone https://github.com/eetuhoo/azure-role-based-assistant.git
cd azure-role-based-assistant
```
2. Create virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create .env file for environment variables:
```bash
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_DEPLOYMENT=...
AZURE_OPENAI_API_VERSION=...
AZURE_SEARCH_ENDPOINT=...
AZURE_SEARCH_API_KEY=...
AZURE_SEARCH_INDEX=...
```
## How to run
```bash
uvicorn main:app --reload
```
Test API endpoint /rag-ask in e.g. Swagger-documentation:
```bash
http://localhost:8000/docs
POST /rag-ask
{
  "role": "IT",
  "question": "Kuinka uusin salasanani?"
}
```
The backend should respond with a role-specific answer.

