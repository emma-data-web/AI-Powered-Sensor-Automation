
import os
from sqlalchemy import MetaData
from database import Database
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("database_url")

if not DATABASE_URL:
    raise ValueError("No database URL found. Set 'database_url' in your .env file.")


database = Database(DATABASE_URL)


metadata = MetaData()
