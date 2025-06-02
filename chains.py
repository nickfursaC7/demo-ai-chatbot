from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from prompt_manager import PromptManager

class ChainManager:
    def __init__(self):
        self.prompt_manager = PromptManager()
        self.db = FAISS.load_local("model", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        self.llm = ChatOpenAI(temperature=0.0, model_name="gpt-4.1-mini")
        self.llm_prep = ChatOpenAI(temperature=0.0, model_name="gpt-4.1-nano")
        self.intent_chain = self.get_chain("intent")
    
    def get_chain(self, intent: str):
        if intent == "intent":
            qa_chain = self.prompt_manager.get_prompt("intent") | self.llm_prep
        elif intent in {"research", "wallet", "unknown"}:
            qa_chain = self.prompt_manager.get_prompt(intent) | self.llm
        else:
            raise ValueError(f"Unknown intent: {intent}")
        return qa_chain