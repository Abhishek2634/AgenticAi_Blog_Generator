from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()

    def get_llm(self):
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            llm = ChatGroq(
                api_key=groq_api_key, 
                model="llama3-70b-8192"  
            )
            return llm
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")
