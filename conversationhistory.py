from langchain.schema import HumanMessage, AIMessage

class ConversationHistory:
    MAX_TOKENS = 1024
    TOKEN_BUFFER = 500

    def __init__(self):
        self.user_conversation_histories = {}
    
    def get_token_count(self, messages):
        return sum(len(message.content.split()) for message in messages)

    #implement add_conversation
    def add_conversation(self, user_id, human_message, ai_message):
        if user_id not in self.user_conversation_histories:
            self.user_conversation_histories[user_id] = []
        self.user_conversation_histories[user_id].append(HumanMessage(content=human_message))
        self.user_conversation_histories[user_id].append(AIMessage(content=ai_message))
        self.truncate_conversation(user_id)

    #implement retrieve_conversation
    def retrieve_conversation(self, user_id):
        history = self.user_conversation_histories.get(user_id, [])

        conversation_history = ''
        for message in history:
            if isinstance(message, HumanMessage):
                conversation_history += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                conversation_history += f"Assitant: {message.content}\n"
        return conversation_history

    #implement truncate_conversation
    def truncate_conversation(self, user_id):
        history = self.user_conversation_histories.get(user_id, [])
        while self.get_token_count(history) > (self.MAX_TOKENS - self.TOKEN_BUFFER):
            history.pop(0)