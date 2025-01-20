from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from core.settings import Settings
from models.conversation import Conversation
from services.prompting import get_initial_prompt_template, get_prompt_template_with_user_message_and_all_previous_messages, get_prompt_template_with_summary_and_recent_messages, get_prompt_template_to_summarize_conversation, get_prompt_template_to_accumulate_summary
import os

AUTH_TOKEN = Settings().auth_token
ENDPOINT_URL = Settings().endpoint_url
os.environ["HUGGINGFACEHUB_API_TOKEN"] = AUTH_TOKEN

llm = HuggingFaceEndpoint(
    endpoint_url=ENDPOINT_URL,
    model_kwargs={
        "max_length":4096, 
    },
    temperature=0.2,         
    do_sample=True,         
    top_k=50,               
    top_p=0.95,             
    return_full_text=False
)

def get_initial_response(user_message:str):
    prompt_template = get_initial_prompt_template()
    llm_chain = prompt_template | llm | StrOutputParser()
    response = llm_chain.invoke({"user_message": user_message})
    return response

def get_response_with_user_message_and_all_previous_messages(user_message:str, conversation:Conversation):
    prompt_template = get_prompt_template_with_user_message_and_all_previous_messages()
    previous_messages = "\n".join([f"User: {message.user_message}\nAssistant: {message.assistant_answer}\n" for message in conversation.messages])
    llm_chain = prompt_template | llm | StrOutputParser()
    response = llm_chain.invoke({"user_message": user_message, "previous_messages": previous_messages})
    return response

def get_summary_of_complete_conversation(conversation:Conversation):
    prompt_template = get_prompt_template_to_summarize_conversation()
    full_history = "\n".join([f"User: {message.user_message}\nAssistant: {message.assistant_answer}\n" for message in conversation.messages])
    llm_chain = prompt_template | llm | StrOutputParser()
    response = llm_chain.invoke({"full_history": full_history})
    return response

def get_accumulated_summary_of_conversation(conversation:Conversation):
    prompt_template = get_prompt_template_to_accumulate_summary()
    summary = conversation.last_summary
    last_interaction = conversation.messages[-1]
    last_user_message = last_interaction.user_message
    last_assistant_answer = last_interaction.assistant_answer
    llm_chain = prompt_template | llm | StrOutputParser()
    response = llm_chain.invoke({"summary": summary, "user_message": last_user_message, "assistant_response": last_assistant_answer})
    return response

def get_response_with_summary_and_recent_messages(user_message:str, conversation:Conversation, summary:str):
    prompt_template = get_prompt_template_with_summary_and_recent_messages()
    recent_messages = "\n".join([f"User: {message.user_message}\nAssistant: {message.assistant_answer}\n" for message in conversation.messages[-10:]])
    llm_chain = prompt_template | llm | StrOutputParser()
    response = llm_chain.invoke({"user_message": user_message, "summary": summary, "recent_messages": recent_messages})
    return response