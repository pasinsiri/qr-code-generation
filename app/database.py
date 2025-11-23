import os
from database import Database
from sqlalchemy import create_engine, MetaData

# * Setup database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/qrdb")
databse = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)