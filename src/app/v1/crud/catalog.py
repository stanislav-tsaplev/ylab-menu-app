from ..db.catalog import fetch_catalog
from ..models.catalog import Catalog


def read_catalog() -> Catalog:
    catalog_json = fetch_catalog()
    return Catalog.from_dict(catalog_json)
