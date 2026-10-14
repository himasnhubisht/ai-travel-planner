from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os 
load_dotenv()

model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


llm = ChatOpenAI(
    model=model_name,
    temperature=0.3,
)
