# Chatbot Demo Documentation

This documentation outlines the training and deployment process of the chatbot demo project, utilizing FAISS for vector storage and OpenAI’s LLM API.

Table of Contents

[Project Overview](#1-project-overview)  
[Dependencies](#2-dependencies)  
[Training Process](#3-training-process)  
* [Data Preparation](#data-preparation)
* [Embedding and Indexing](#embedding-and-indexing)

[Inference API](#4-inference-api)  
* [Setup and Initialization](#setup-and-initialization)
* [Endpoints](#endpoints)
* [Testing the API](#testing-the-api)

[Deployment](#5-deployment)
[Future Improvements](#6-future-improvements)

## 1. Project Overview

This chatbot demonstrates the integration of OpenAI’s GPT-4 model with a custom dataset for domain-specific query responses. The project features:  
- A training pipeline that indexes data using FAISS.  
- An inference API built with FastAPI.  

## 2. Dependencies

Ensure the following Python packages are installed:

```bash
pip install -r requirements.txt
```

Key dependencies:  
- langchain  
- faiss-cpu or faiss-gpu  
- openai  
- fastapi  
- uvicorn  

## 3. Training Process

### Data Preparation

Prepare your dataset:  
1.	Store articles or domain-specific documents in the folder.  
2.	Each document should have:  
    - A .txt file as the file extension.  
    - Metadata added at the top of the file (e.g., title, URL).

The structure may look like:

data/
```text
├── document1.txt
    Title: Sample Title
    URL: https://example.com/article1

    <document content>
    
├── document2.txt
    Title: Another Title
    URL: https://example.com/article2

    <document content>
```

### Embedding and Indexing

Use the training script in train.ipynb to generate vector embeddings and save the FAISS index.  
1.	Load Data:
```py
from langchain.schema import Document
from pathlib import Path
import json

def load_data():
    data_path = Path("data")
    documents = []
    for file_path in data_path.glob("*.txt"):
        with open(file_path, "r") as f:
            content = f.read()
        documents.append(Document(page_content=content))
    return documents
```

2.	Generate FAISS Index:
```py
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

documents = load_data()
embeddings = OpenAIEmbeddings(openai_api_key="YOUR_OPENAI_API_KEY")
faiss_index = FAISS.from_documents(documents, embeddings)
faiss_index.save_local("model")
```
## 4. Inference API

The inference pipeline is implemented in handler.py.

### Setup and Initialization
1.	Load the FAISS index:
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key="YOUR_OPENAI_API_KEY")
db = FAISS.load_local("model", embeddings)
```

2.	Create a retriever and connect it to a QA pipeline:
```py
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

retriever = db.as_retriever()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
```


### Endpoints

The API exposes the following endpoints:  
POST /ask/  
Accepts a query and returns a response based on the indexed data.  

- Input:  
```json
{
  "user_id": "user_123",
  "query": "What is the fastest way to achieve Marriott Bonvoy elite status?"
}
```
  
- Response:  
```json
{
  "query": "What is the fastest way to achieve Marriott Bonvoy elite status?",
  "resp": "The fastest way is to..."
}
```

## 5. Deployment

Environment Setup
1.	Install Python 3.12:  
Follow the steps in server_steps.md to install Python 3.12 and dependencies on an AWS EC2 instance.
2.	Copy Files:  
Upload the model files and handler.py to the server:  
```bash
scp -i chatbot-ec2.pem model/* ec2-user@<EC2_IP>:~/chatbot/model
scp -i chatbot-ec2.pem handler.py ec2-user@<EC2_IP>:~/chatbot/
```

3.	Start the Server:

### Testing the API

Run the server:
```bash
uvicorn handler:app --host 0.0.0.0 --port 8000
```
Test with curl:
```py
curl --location 'http://localhost:8000/ask/' \
--header 'Content-Type: application/json' \
--data '{"query": "Tell me about Delta lounges"}'
```

## 6. Future Improvements  
1.	Scalability:
- Use faiss-gpu for larger datasets.
- Implement caching for frequent queries.
2.	Features:
- Context maintenance
- Multi-user support
- Add user authentication.
- Enable fine-tuning of the OpenAI model for domain-specific data.
3.	Monitoring:
- Integrate with monitoring tools (e.g., Prometheus, Grafana).

