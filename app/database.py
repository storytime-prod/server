from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select


from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True, connect_args={"sslmode": "require"})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# Test connection
def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Connected to the database successfully!", connection)
    except Exception as e:
        print("❌ Database connection failed:")
        print(e)
