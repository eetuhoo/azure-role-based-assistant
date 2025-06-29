from fastapi import FastAPI
from pydantic import BaseModel
from prompts import get_prompt
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os

from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"), 
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

credential = AzureKeyCredential(key)
search_client = SearchClient(endpoint, index_name, credential)


deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

app = FastAPI()

class Query(BaseModel):
    role: str
    question: str

@app.post("/ask/")
def ask(query: Query):
    with open("knowledge/hr_faq.txt") as f:
        knowledge = f.read()

    prompt = get_prompt(query.role, query.question, knowledge)
    
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return {"response": response.choices[0].message.content}

@app.post("/rag-ask")
async def rag_ask(query: Query):
    question = query.question

    results = search_client.search(question, top=3)

    context = "\n\n".join(
        f"{doc['question']}\n{doc['answer']}"
        for doc in results
    )

    prompt = get_prompt(query.role, query.question, context)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return {"response": response.choices[0].message.content}
