from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import db_engine
from ..models import Menu, Submenu, Dish


async def fetch_catalog():
    async with AsyncSession(db_engine) as session:
        submenus_query = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                Submenu.menu_id,
                func.json_agg(
                    func.json_build_object(
                        "title",
                        Dish.title,
                        "description",
                        Dish.description,
                        "price",
                        Dish.price,
                    )
                ).label("dishes"),
            )
            .join(Dish, isouter=True)
            .where(Submenu.id == Dish.submenu_id)
            .group_by(Submenu.id)
        )

        menus_query = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.json_agg(
                    func.json_build_object(
                        "title",
                        submenus_query.c.title,
                        "description",
                        submenus_query.c.description,
                        "dishes",
                        submenus_query.c.dishes,
                    )
                ).label("submenus"),
            )
            .where(Menu.id == submenus_query.c.menu_id)
            .group_by(Menu.id)
        )

        catalog_query = select(
            func.json_agg(
                func.json_build_object(
                    "title",
                    menus_query.c.title,
                    "description",
                    menus_query.c.description,
                    "submenus",
                    menus_query.c.submenus,
                )
            ).label("menus")
        )

        db_catalog = (
            await session.exec(
                select(
                    func.json_build_object("menus", catalog_query.c.menus).label(
                        "catalog"
                    )
                )
            )
        ).one()
        return db_catalog
