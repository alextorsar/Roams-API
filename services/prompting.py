from langchain.prompts import PromptTemplate

def get_initial_prompt_template():
    """
    Generates the initial prompt template to start a conversation.
    This template does not include any prior conversation history, 
    only the user's query.

    Returns:
        PromptTemplate: Initial prompt template for the model.
    """
    return PromptTemplate(
        input_variables=["user_message"],
        template="""
        You are an intelligent assistant. A user has started a conversation with you. 
        He just said: "{user_message}"
        
        Your goal is to assist him in the best way possible. Begin by responding politely and providing 
        a clear and helpful answer. If additional clarification is needed, ask follow-up questions to 
        better understand his needs.
        
        Respond only with your answer as an assistant, anything else. Your response:
        """
    )

def get_prompt_template_with_user_message_and_all_previous_messages():
    """
    Generates a prompt template that includes all previous messages from the conversation
    along with the user's current query.

    Returns:
        PromptTemplate: Prompt template containing the full message history and the user's query.
    """
    return PromptTemplate(
        input_variables=["user_message", "previous_messages"],
        template="""
        You are an intelligent assistant. You are having a conversation with a user and your goal is to assist him 
        in the best way possible. This is the ongoing conversation between the user and you (The Assistant):
        
        {previous_messages}
        
        The user just said: "{user_message}"
        
        Based on the context above, respond appropriately to the user's query, 
        maintaining the tone and relevance of the conversation. If additional clarification is needed, ask follow-up
        questions to better understand their needs.
        
        Respond only with your answer as an assistant, anything else. Your response:
        """
    )

def get_prompt_template_with_summary_and_recent_messages():
    """
    Combines a previously generated summary and recent messages
    (last 10 messages) with the user's query to form the prompt template.

    Returns:
        PromptTemplate: Prompt template with the summary, the last 10 messages, and the user's query.
    """
    return PromptTemplate(
        input_variables=["user_message", "summary", "recent_messages"],
        template="""
        You are an intelligent assistant. You are having a conversation with a user and your goal is to assist him 
        in the best way possible. Below is a summary of the previous conversation along with the most recent messages:

        Summary of the previous conversation:
        {summary}

        Recent messages between the user and you (The Assistant):
        {recent_messages}

        The user has just said: "{user_message}"

        Based on the summary and the recent messages, provide a clear and helpful response to the user's query. 
        Make sure your response is relevant to the context and maintains the tone of the conversation. 
        If further clarification is needed, ask follow-up questions to better understand the user's needs.
        
        Respond only with your answer as an assistant, anything else. Your response:
        """
    )

def get_prompt_template_to_summarize_conversation():
    """
    Generates a prompt template to summarize the entire conversation history.

    Returns:
        PromptTemplate: Prompt template to summarize the entire conversation.
    """
    return PromptTemplate(
        input_variables=["full_history"],
        template="""
        You are an intelligent assistant. Below is the full conversation history between a user and you (The Assistant):

        {full_history}

        Your task is to summarize the conversation into a concise and coherent summary that captures:
        - The main topics discussed.
        - The user's questions and goals.
        - The assistant's answers and key points.

        The summary must be detailed enough to provide all the necessary context so that, if needed, it could be used 
        as the only reference to answer any future question related to this conversation. Focus on clarity and relevance, 
        and omit unnecessary details or repetitions.
        
        Respond only with your summary as an assistant, anything else. Your summary:
        """
    )

def get_prompt_template_to_accumulate_summary():
    """
    Generates a prompt template to update a summary of the conversation history with the last message.

    Returns:
        PromptTemplate: Prompt template to accumulate a summary of the conversation.
    """
    return PromptTemplate(
        input_variables=["summary", "user_message", "assistant_response"],
        template="""
        You are an intelligent assistant tasked with summarizing a conversation. 
        Below is the current summary of the conversation so far, followed by the latest interaction:

        Current summary:
        {summary}

        Latest interaction:
        User: "{user_message}"
        Assistant: "{assistant_response}"
        
        Your task is to update the summary to include the latest interaction while keeping it concise 
        and focused on the key points. It should capture:
        
        - The main topics discussed so far, including the new information from the latest interaction.
        - The user's questions and goals.
        - The assistant's answers and key points.

        Maintain clarity and relevance, and omit unnecessary details.
        
        Respond only with your summary as an assistant, anything else. Your summary:
        """
    )