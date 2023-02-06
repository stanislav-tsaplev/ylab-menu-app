from .. import db


async def read_catalog() -> dict:
    catalog_json = await db.fetch_catalog()
    return catalog_json
