import os
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

credential = AzureKeyCredential(key)

# Create index
index_client = SearchIndexClient(endpoint, credential)

if __name__ == "__main__":
    
    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SimpleField(name="source", type="Edm.String", filterable=True),
        SearchableField(name="question", type="Edm.String", analyzer_name="en.lucene"),
        SearchableField(name="answer", type="Edm.String", analyzer_name="en.lucene")
    ]
    index = SearchIndex(name=index_name, fields=fields)
    index_client.create_index(index)
    print(f"Index '{index_name}' created.")

    search_client = SearchClient(endpoint, index_name, credential)

    files = ["../knowledge/hr_faq.txt", "../knowledge/it_faq.txt", "../knowledge/security_faq.txt"]

    documents = []
    doc_id = 0
    delimiter = '|'

    # Create documents payload
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line or delimiter not in line:
                    continue
                faq, answer = line.split(delimiter, 1)
                documents.append({
                    "id": str(doc_id),
                    "source": file_path,
                    "question": faq.strip(),
                    "answer": answer.strip()
                })
                doc_id += 1

    # Upload documents
    if documents:
        result = search_client.upload_documents(documents)
        print(f"Uploaded {len(result)} documents successfully.")
    else:
        print("Nothing to upload.")