import os
from databases import Database
from sqlalchemy import create_engine, MetaData

# * Setup database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./local.db")

# databases library needs the URL with the async driver
database = Database(DATABASE_URL)
metadata = MetaData()

# SQLAlchemy engine needs the sync driver URL
SYNC_DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite", "sqlite").replace("postgresql+asyncpg", "postgresql")
engine = create_engine(SYNC_DATABASE_URL)