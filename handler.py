import json
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import helpers as h
from chains import ChainManager

logging.getLogger().setLevel(logging.INFO)

app = FastAPI()

chain = ChainManager()
db = chain.db
intent_chain = chain.get_chain("intent")

class Query(BaseModel):
    query: str
    user_id: str

@app.post("/ask/")
def ask(request: Query):
    user_id = request.user_id
    query = request.query
    intent = intent_chain.invoke({"query": query}).content
    logging.info(f"User {user_id} asked: {query}\nIntent: {intent}")
    
    if intent == "research":
        research_chain = chain.get_chain("research")
        search_results = db.similarity_search_with_score(query=query, k=3, score_threshold=0.5)
        docs = [doc for doc in search_results]

        log_line = '\n' + \
            '\n'.join([', '.join([str(round(score, 3)), doc.metadata['title']])
                    for doc, score in search_results])
        logging.info(f"Retrieved docs: {log_line}")

        input_params = {
            "qa_chain": research_chain,
            "conversation_history": h.CH.retrieve_conversation(user_id),
            "context": docs,
            "query": query,
        }
    elif intent == "wallet":
        
        #test user data (to be replaced with actual user data retrieval)
        with open("test_user_data.json", "r") as f:
            user_data = json.load(f)
        
        wallet_chain = chain.get_chain("wallet")
        input_params = {
            "qa_chain": wallet_chain,
            "conversation_history": h.CH.retrieve_conversation(user_id),
            "user_data": user_data,
            "query": query,
        }
    elif intent == "unknown":
        unknown_chain = chain.get_chain("unknown")
        input_params = {
            "qa_chain": unknown_chain,
            "conversation_history": h.CH.retrieve_conversation(user_id),
            "context": [],
            "query": query,
        }
    else:
        raise ValueError(f"Unknown intent: {intent}")

    response = h.run_conversation(**input_params)
    logging.info(f"UserID {user_id}\nResponse: {response}")

    body = {
        "query": query,
        "response": response,
    }

    response = {
        "statusCode": 200,
        "body": body,
    }

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)