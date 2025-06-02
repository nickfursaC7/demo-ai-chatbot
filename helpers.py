from conversationhistory import ConversationHistory

CH = ConversationHistory()

def create_context(docs):
    return "\n".join([doc[0].page_content for doc in docs])

def run_conversation(**input_params):
    user_id = input_params.get("user_id")
    query = input_params.get("query")
    qa_chain = input_params.get("qa_chain")
    docs = input_params.get("context")
    user_data = input_params.get("user_data", {})
    #retrieve conversation
    conversation_history = CH.retrieve_conversation(user_id)

    params = {
        "query": query,
        "user_data": user_data,
        "conversation_history": conversation_history
    }

    #implement context
    if docs:
        params["context"] = create_context(docs)

    #run QA chain
    response = qa_chain.invoke(params)

    #update conversation history
    CH.add_conversation(user_id, query, response.content)

    #return answer
    return response.content