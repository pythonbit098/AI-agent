from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from langchain import LLMChain, PromptTemplate

from .models import Base, Expense

class ExpenseTracker:
    def __init__(self, llm, database_url, api_key):
        # Set up API key for the LLM
        import os
        if not os.environ.get("GROQ_API_KEY"):
            os.environ["GROQ_API_KEY"] = api_key
        
        # Set up the LLM and database
        self.llm = llm
        self.database_url = f"sqlite:///{database_url}.db"
        
        # Create the database engine
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        # Prompt template
        self.prompt_template = """
        You are an assistant that extracts expense details from the user's input.
        The input is: {user_input}
        Extract the amount, category, and current date based on your knowledge.

        **always double check if the data's are extracted properly**
        your response always needs to be like **example: Amount: 100, Category: food.**
        If can't find Category, return Category: unknown.
        """

    def extract(self, user_input):
        # Create a new session
        session = self.Session()
        
        # Prepare the LLM chain
        prompt = PromptTemplate(input_variables=["user_input"], template=self.prompt_template)
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # Get LLM response
        response = llm_chain.run(user_input)
        
        # Extract amount and category from the response
        amount = int(response.split("**")[1].split(",")[0].split(":")[1].strip())
        category = response.split("**")[1].split(",")[1].split(":")[1].strip()
        date = datetime.today().date()
        
        # Handle unknown category
        if category.lower() == "unknown":
            category = input("Which category does this spending come under? ")
        
        # Save to the database
        new_expense = Expense(date=date, category=category, amount=amount)
        session.add(new_expense)
        session.commit()
        
        return f"Expense added: {amount} spent on {category}."
