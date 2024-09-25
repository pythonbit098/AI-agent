from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .config import DATABASE_URL

# Create a database engine
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
