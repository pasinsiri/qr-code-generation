from .database import database, qrs
from .models import qrs

async def create_qr(short_code: str, url: str, title: str):
    query = qrs.insert().values(short_code=short_code, url=url, title=title)
    return await database.execute(query)

async def get_qr_by_code(short_code: str):
    query = qrs.select().where(qrs.c.short_code == short_code)
    return await database.fetch_one(query)

async def increment_clicks(short_code: str, ip: str):
    # Very simple unique detection
    query = qrs.update().where(qrs.c.short_code == short_code)
    return await database.execute(query.values(
        total_clicks=qrs.c.total_clicks + 1,
        unique_clicks=qrs.c.unique_clicks + databases.sql.literal_column(
            "CASE WHEN unique_clicks = 0 OR NOT (unique_clicks::text LIKE '%' || %s || '%') THEN 1 ELSE 0 END", ip
        )
    ))
    # Note: For real unique tracking, use a separate clicks table