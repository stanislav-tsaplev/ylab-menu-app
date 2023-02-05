from .. import db
from ..models.catalog import Catalog


async def read_catalog() -> Catalog:
    catalog_json = await db.fetch_catalog()
    return Catalog.from_dict(catalog_json)
