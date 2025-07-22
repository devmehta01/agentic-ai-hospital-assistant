from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="mistral")

prompt = PromptTemplate.from_template("""
You are an intent classification assistant for a hospital chatbot.

Classify the user message into one of these categories:
- book_appointment: if the user wants to book a new appointment
- change_appointment: if the user wants to change, cancel, or reschedule an existing appointment
- ask_info: if the user is asking for hospital-related information (like insurance, timings, services, etc.)

User message: {user_input}

Reply with only one of the following:
book_appointment, change_appointment, ask_info
""")

intent_chain: Runnable = prompt | llm | StrOutputParser()

def classify_intent(user_input: str) -> str:
    return intent_chain.invoke({"user_input": user_input}).strip().lower()