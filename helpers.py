from conversationhistory import ConversationHistory

CH = ConversationHistory()

def create_context(docs):
    return "\n".join([doc[0].page_content for doc in docs])

def run_conversation(qa_chain, user_id, query, docs):
    #retrieve conversation
    conversation_history = CH.retrieve_conversation(user_id)

    #implement context
    context = create_context(docs)

    #run QA chain
    response = qa_chain.invoke({
        "conversation_history": conversation_history,
        "context": context,
        "query": query,
    })

    #update conversation history
    CH.add_conversation(user_id, query, response.content)

    #return answer
    return response.content