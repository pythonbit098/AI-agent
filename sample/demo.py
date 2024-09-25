from expense_tracker import ExpenseTracker
from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = "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"

# Initialize the LLM model
llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# Initialize the ExpenseTracker with the LLM, database URL, and API key
expense_tracker = ExpenseTracker(
    llm=llm,
    database_url='expense'
)

# Use the expense_tracker to extract and store an expense
print(expense_tracker.extract("I spent 2000 for food today"))
