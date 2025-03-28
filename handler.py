from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import helpers as h

logging.getLogger().setLevel(logging.INFO)

app = FastAPI()

custom_prompt = PromptTemplate(
    template=(
        "You are a helpful assistant answering questions based on retrieved documents and past conversation.\n\n"
        "If available, provide URL links to the source of the information.\n\n"
        "Make sure to review the context when providing relevant information.\n\n"
        "If you don't know the answer, just say that you don't know. Don't try to make up an answer.\n\n"

        "IMPORTANT: Preserve the original case of any URLs in your response.\n\n"

        "Conversation History: {conversation_history}\n\n"
        "Context: {context}\n\n"
        "Question: {query}\n"
        "Answer:"
    ),
    input_variables=["conversation_history", "context", "query"],
)

db = FAISS.load_local("model", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
llm = ChatOpenAI(temperature=0.0, model_name="gpt-4o-mini")
qa_chain = custom_prompt | llm

class Query(BaseModel):
    query: str
    user_id: str

@app.post("/ask/")
def ask(request: Query):
    user_id = request.user_id
    query = request.query
    logging.info(f"User {user_id} asked: {query}")
    docs =db.similarity_search_with_score(query=query, k=3, score_threshold=0.5)
    log_line = '\n'+'\n'.join([', '.join([str(round(score, 3)), doc.metadata["title"]]) for doc, score in docs])
    logging.info(f"Retrieved documents: {log_line}")

    response = h.run_conversation(qa_chain, user_id, query, docs)
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