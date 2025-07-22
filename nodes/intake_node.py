from langchain_core.runnables import Runnable
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="mistral")

prompt = PromptTemplate.from_template("""
You are a medical assistant helping a hospital intake system.

Extract the following from the user's message:
- full name
- driver license number
- symptoms (as a comma-separated list)

Only reply in this exact JSON format:
{{"name": "...", "license": "...", "symptoms": "..."}}

User input: {user_input}
""")

output_parser = JsonOutputParser()
intake_chain: Runnable = prompt | llm | output_parser

def extract_intake_details(user_input: str) -> dict:
    return intake_chain.invoke({"user_input": user_input})