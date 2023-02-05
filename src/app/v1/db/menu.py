from uuid import UUID

from sqlmodel import delete, select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import db_engine
from ..models.menu import Menu, MenuCreate, MenuUpdate


async def create_menu(menu_creating_data: MenuCreate) -> Menu:
    """Create a new menu with the creating values.

    Return newly created `Menu` object
    """
    async with AsyncSession(db_engine) as session:
        db_menu = Menu.from_orm(menu_creating_data)
        session.add(db_menu)

        await session.commit()
        await session.refresh(db_menu)

        return db_menu


async def update_menu(menu_id: UUID, menu_updating_data: MenuUpdate) -> Menu | None:
    """Update the menu with the updating values.

    Return the updated `Menu` object,when `menu_id` is a valid menu id
    or `None` otherwise
    """
    async with AsyncSession(db_engine) as session:
        db_menu = (
            await session.exec(select(Menu).where(Menu.id == menu_id))
        ).one_or_none()

        if db_menu is None:
            return None

        await session.exec(
            update(Menu)
            .where(Menu.id == menu_id)
            .values(**menu_updating_data.dict(exclude={"id"}, exclude_unset=True))
        )

        await session.commit()
        await session.refresh(db_menu)

        return db_menu


async def delete_menu(menu_id: UUID) -> None:
    async with AsyncSession(db_engine) as session:
        await session.exec(delete(Menu).where(Menu.id == menu_id))
        await session.commit()


async def read_menu(menu_id: UUID) -> Menu | None:
    async with AsyncSession(db_engine) as session:
        db_menu = await session.get(Menu, menu_id)
        if db_menu is None:
            return None

        return db_menu


async def read_all_menus() -> list[Menu]:
    async with AsyncSession(db_engine) as session:
        db_menus = (await session.exec(select(Menu))).all()
        return db_menus
