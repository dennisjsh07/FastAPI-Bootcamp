from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() # read the dotenv file

db_url = os.getenv("DATABASEURL")
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)