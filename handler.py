from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = FAISS.load_local("model", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
retriever = db.as_retriever()
llm = ChatOpenAI(temperature=0.0, model_name="gpt-4o-mini")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

class Query(BaseModel):
    query: str

@app.post("/ask/")
def ask(request: Query):
    response = qa.invoke({'query':request.query})
    return response.get('result')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)