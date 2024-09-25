import os
from langchain_groq import ChatGroq

# Set your Groq API Key
os.environ["GROQ_API_KEY"] = "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"

# LLM configuration
llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# Database connection string
DATABASE_URL = 'sqlite:///expense.db'
