from intent_template import intent_template
from research_template import research_template
from wallet_template import wallet_template
from unknown_template import unknown_template
from typing import Literal, Dict
from langchain.prompts import PromptTemplate

class PromptManager:
    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {
            "intent": intent_template,
            "research": research_template,
            "wallet": wallet_template,
            "unknown": unknown_template
        }
    
    def get_prompt(self, prompt_type: Literal["intent", "research", "wallet", "unknown"]) -> PromptTemplate:
        return self.prompts[prompt_type]