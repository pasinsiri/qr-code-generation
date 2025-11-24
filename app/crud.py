from .database import database
from .models import qrs

async def create_qr(short_code: str, url: str, title: str):
    query = qrs.insert().values(short_code=short_code, url=url, title=title, total_clicks=0, unique_clicks=0)
    return await database.execute(query)

async def get_qr_by_code(short_code: str):
    query = qrs.select().where(qrs.c.short_code == short_code)
    return await database.fetch_one(query)

async def increment_clicks(short_code: str, ip: str):
    # Very simple unique detection - just increment total clicks
    # For production, use a separate clicks table to track unique visitors
    query = qrs.update().where(qrs.c.short_code == short_code).values(
        total_clicks=qrs.c.total_clicks + 1,
        unique_clicks=qrs.c.unique_clicks + 1
    )
    return await database.execute(query)