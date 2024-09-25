import os
from sqlalchemy import create_engine, Column, Integer, String, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Integer)

# Create a database engine
engine = create_engine('sqlite:///expense.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

llm = ChatGroq(model="llama3-8b-8192", temperature=0)

prompt_template = """
You are an assistant that extracts expense details from the user's input. 
The input is: {user_input}
Extract the amount, category, and current date based on your knowledge.

For Example: if the user gives the input like "i have spend 100 for food today"
    Then you have to extract the data like Amount: 100 and the category: "Food" form the user input.

**always double check if the data's are extracted properly**

your response always need to like **example: Amount: 100, Category: food.**
only the amount and the category and always use ** before and after the Amount and Category text
** if can't able to find Category then return Category: unknown ** 

"""

def extract_expense(user_input):
    prompt = PromptTemplate(input_variables=["user_input"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    response = llm_chain.invoke(user_input)
    

    # print(response)
    # return response
    # Parsing the output (You may adjust parsing based on Llama's output)
    amount = int(response.split("**")[1].split(",")[0].split(":")[1].strip())
    category = response.split("**")[1].split(",")[1].split(":")[1].strip()
    date = datetime.today().date()
    
    # If the category is unclear, the agent will ask the user for clarification.
    if category.lower() == "unknown":
        category = input("Which category does this spending come under? ")
    
    # Save the extracted data to the SQL database
    new_expense = Expense(date=date, category=category, amount=amount)
    session.add(new_expense)
    session.commit()
    
    return f"Expense added: {amount} spent on {category}."

test_inputs = [
    "Today I spent 150 on groceries.",
    "I paid 500 for rent this week.",
    "Yesterday I spent 80 on car fuel.",
    "I bought a new phone for 12000.",
    "Spent 200 on a restaurant with friends last night.",
    "Paid 300 for my internet bill today.",
    "I spent 50 on public transport this morning.",
    "I had to pay 400 for health insurance.",
    "I spent 1000 on clothing during the weekend.",
    "Spent 150 on subscriptions last month."
]

for i in test_inputs:
    print(extract_expense(i))