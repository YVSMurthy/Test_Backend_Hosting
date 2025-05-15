from sqlalchemy import create_engine #type: ignore
from sqlalchemy.orm import sessionmaker #type: ignore
from dotenv import load_dotenv #type: ignore
import os
from .schema import Base

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
POOLMODE = os.getenv("pool_mode")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables (only for initial setup or development)
Base.metadata.create_all(bind=engine)
