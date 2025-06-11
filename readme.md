# Chatbot Demo Documentation

This documentation outlines the training and deployment process of the chatbot demo project, utilizing FAISS for vector storage, OpenAI's LLM API, and intelligent intent routing with multi-level prompting.

Table of Contents

[Project Overview](#1-project-overview)  
[Dependencies](#2-dependencies)  
[Architecture](#3-architecture)
* [Intent Classification](#intent-classification)
* [Multi-level Prompting](#multi-level-prompting)
* [Conversation History Management](#conversation-history-management)

[Training Process](#4-training-process)  
* [Data Preparation](#data-preparation)
* [Embedding and Indexing](#embedding-and-indexing)

[Inference API](#5-inference-api)  
* [Setup and Initialization](#setup-and-initialization)
* [Intent Routing](#intent-routing)
* [Endpoints](#endpoints)
* [Testing the API](#testing-the-api)

[Deployment](#6-deployment)
[Future Improvements](#7-future-improvements)

## 1. Project Overview

This chatbot demonstrates an advanced architecture featuring:  
- **Intent-based routing** to classify user queries into specific categories
- **Multi-level prompting** with specialized templates for different use cases
- **Conversation history management** for contextual responses
- **FAISS vector storage** for semantic search over documents
- **FastAPI-based inference** with OpenAI's GPT-4 integration

The system intelligently routes queries to specialized handlers:
- **Research**: Questions about loyalty programs and travel (with document retrieval)
- **Wallet**: Personal points/miles management and redemption recommendations
- **Unknown**: General travel-related queries or redirection

## 2. Dependencies

Ensure the following Python packages are installed:

```bash
pip install -r requirements.txt
```

Key dependencies:  
- langchain  
- langchain-openai
- langchain-community
- faiss-cpu or faiss-gpu  
- openai  
- fastapi  
- uvicorn
- python-dotenv
- pydantic

## 3. Architecture

### Intent Classification

The system uses a two-stage approach:
1. **Intent Classification**: A lightweight model (`gpt-4.1-nano`) classifies queries into:
   - `research`: Learning about loyalty programs
   - `wallet`: Using personal points/miles for redemptions
   - `unknown`: General travel questions or off-topic queries

2. **Specialized Processing**: Each intent routes to a specialized chain with tailored prompts

```python
# Intent classification prompt
intent_template = PromptTemplate(
    template=(
        "You are an intent classifier. Classify the user query into one of the following categories:\n"
        "- 'research': if the user is asking to learn about points/miles or loyalty programs\n"
        "- 'wallet': when user is interested in the best use of miles and points in their wallets\n"
        "- 'unknown': if it's unclear or doesn't fit above\n\n"
        "User Query: {query}\n"
        "Intent:"
    ),
    input_variables=["query"],
)
```

### Multi-level Prompting

The system uses specialized prompt templates for each intent:

**Research Template**: For educational queries with document retrieval
- Includes context from FAISS similarity search
- Emphasizes providing source URLs
- Structured Markdown formatting

**Wallet Template**: For personal redemption optimization
- Accesses user's points/miles data
- Provides personalized recommendations
- Considers home airport and preferences

**Unknown Template**: For general or off-topic queries
- Maintains focus on travel/loyalty topics
- Politely redirects non-travel questions

### Conversation History Management

```python
class ConversationHistory:
    MAX_TOKENS = 1024
    TOKEN_BUFFER = 500
    
    def add_conversation(self, user_id, human_message, ai_message)
    def retrieve_conversation(self, user_id)
    def truncate_conversation(self, user_id)
```

Features:
- Per-user conversation tracking
- Token-based truncation to stay within limits
- Maintains context across multiple interactions

## 4. Training Process

### Data Preparation

Prepare your dataset:  
1.	Store articles or domain-specific documents in the data folder.  
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
embeddings = OpenAIEmbeddings()
faiss_index = FAISS.from_documents(documents, embeddings)
faiss_index.save_local("model")
```

## 5. Inference API

The inference pipeline is implemented across multiple modules for better organization:

### Setup and Initialization

**Chain Manager** (`chains.py`):
```python
class ChainManager:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.db = FAISS.load_local("model", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        self.llm = ChatOpenAI(temperature=0.0, model_name="gpt-4.1-mini")
        self.llm_prep = ChatOpenAI(temperature=0.0, model_name="gpt-4.1-nano")
```

**Prompt Manager** (`prompt_manager.py`):
```python
class PromptManager:
    def __init__(self):
        self.prompts = {
            "intent": intent_template,
            "research": research_template,
            "wallet": wallet_template,
            "unknown": unknown_template
        }
```

### Intent Routing

The main handler (`handler.py`) implements the routing logic:

1. **Classify Intent**: Use intent chain to determine query type
2. **Route to Specialized Chain**: Based on intent, select appropriate processing
3. **Retrieve Context**: For research queries, perform similarity search
4. **Process Query**: Run through specialized prompt template
5. **Update History**: Store conversation for future context

```python
# Intent classification
intent = intent_chain.invoke({"query": query}).content

if intent == "research":
    # Retrieve relevant documents
    search_results = db.similarity_search_with_score(query=query, k=3, score_threshold=0.5)
    # Process with research chain
elif intent == "wallet":
    # Load user data and process with wallet chain
elif intent == "unknown":
    # Process with general unknown chain
```

### Endpoints

The API exposes the following endpoints:  
POST /ask/  
Accepts a query and returns a response based on intent routing and specialized processing.

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
  "statusCode": 200,
  "body": {
    "query": "What is the fastest way to achieve Marriott Bonvoy elite status?",
    "response": "### Achieving Marriott Bonvoy Elite Status\n\n**Elite Night Credits** are the primary way to achieve status:\n- **Silver Elite**: 10 elite nights\n- **Gold Elite**: 25 elite nights\n- **Platinum Elite**: 50 elite nights\n- **Titanium Elite**: 75 elite nights\n- **Ambassador Elite**: 100+ nights + $23,000 spend\n\n**Fastest Methods:**\n1. **Credit Card Bonuses**: Marriott credit cards offer automatic elite nights\n2. **Status Challenges**: Some regions offer accelerated earning periods\n3. **Corporate Rates**: Business travelers can earn double elite nights\n\nFor more details: https://www.marriott.com/loyalty/member-benefits/elite.mi"
  }
}
```

### Testing the API

Create a test file with conversation examples:
```python
from handler import ask, Query

# Test different intents
# research
resp1 = ask(Query(query="How to achieve high elite status with Marriott?", user_id="test_user_123"))
# wallet
resp2 = ask(Query(query="How many United miles do I have?", user_id="test_user_123"))
# wallet (no data available in the wallet)
resp3 = ask(Query(query="How many Delta miles do I have?", user_id="test_user_123"))
```

## 6. Deployment

### Environment Setup
1. **Environment Variables**: Create a `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

2. **Install Dependencies**:  
```bash
pip install -r requirements.txt
```

3. **Start the Server**:
```bash
uvicorn handler:app --host 0.0.0.0 --port 8000
```

### Testing the API

Test with curl:
```bash
curl --location 'http://localhost:8000/ask/' \
--header 'Content-Type: application/json' \
--data '{
  "user_id": "test_123",
  "query": "Tell me about Delta lounges"
}'
```

## 7. Future Improvements  

1. **User Experience**:
   - Add streaming responses for real-time interaction
   - Implement typing indicators
   - Add suggested follow-up questions

2. **Monitoring & Analytics**:
   - Track intent classification accuracy
   - Monitor response quality metrics
   - Implement A/B testing for prompt optimization

3. **Security & Privacy**:
   - LLM abuse
   - Implement rate limiting
   - Add PII detection and redaction

