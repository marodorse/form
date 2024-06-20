from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for SQLite (specifies where the database file is located)
DATABASE_URL = "sqlite:///./test.db"

# Create a connection to the SQLite database
engine = create_engine(DATABASE_URL)

# Create a session maker to handle interactions with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for our database models
Base = declarative_base()

# Define a table structure for storing contacts in the database
class Contact(Base):
    __tablename__ = "contacts"  # Table name in the database

    # Columns in the 'contacts' table
    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for each contact
    first_name = Column(String, index=True)  # First name of the contact
    last_name = Column(String, index=True)  # Last name of the contact
    email = Column(String, index=True)  # Email address of the contact
    continent = Column(String, index=True)  # Continent where the contact resides
    message = Column(String, index=True)  # Message sent by the contact
    gender = Column(String, index=True)  # Gender of the contact
    subject = Column(String, index=True)  # Subject of the contact message

# Function to create the database tables based on the defined models
def init_db():
    Base.metadata.create_all(bind=engine)

# Check if this script is run directly (not imported as a module)
if __name__ == "__main__":
    # Initialize the database tables by calling the init_db function
    init_db()
