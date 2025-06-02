from langchain.prompts import PromptTemplate

intent_template = PromptTemplate(
    template=(
        "You are an intent classifier. Classify the user query into one of the following categories:\n"
        "- 'research': if the user is asking to learn about points/miles or loyalty programs\n"
        "- 'wallet': when user is interested in the best use of the miles and points that are already in their wallets. This also may include questions that can be answered with user's data, which includes: first name, home airport, etc. For example:\n"
        "    * 'What can I get with my United miles?', or 'How can I use my Hilton points?', or 'What are the best redemptions for my 200,000 American Express points?', etc.\n"
        "- 'unknown': if it's unclear or doesn't fit above\n\n"
        "User Query: {query}\n"
        "Intent:"
    ),
    input_variables=["query"],
)