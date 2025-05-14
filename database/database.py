from sqlalchemy import create_engine #type: ignore
from sqlalchemy.orm import sessionmaker #type: ignore
from models import Base #type: ignore

DATABASE_URL = "postgresql+psycopg2://user:password@hostname:port/dbname"

# Create the engine (connection) to the database
engine = create_engine(DATABASE_URL)

# Create a sessionmaker that will handle the sessions for us
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database (if they don't exist already)
Base.metadata.create_all(bind=engine)
