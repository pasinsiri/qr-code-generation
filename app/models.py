from sqlalchemy import Table, Column, Integer, String, DateTime, func
from .database import metadata

qrs = Table(
    "qrs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("short_code", String, unique=True, index=True),
    Column("url", String),
    Column("title", String, nullable=True),
    Column("total_clicks", Integer, default=0),
    Column("unique_clicks", Integer, default=0),
    Column("created_at", DateTime, default=func.now()),
)