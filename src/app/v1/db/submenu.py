from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import select, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import db_engine
from ..models.submenu import Submenu, SubmenuCreate, SubmenuUpdate


async def create_submenu(
    menu_id: UUID, submenu_creating_data: SubmenuCreate
) -> Submenu | None:
    async with AsyncSession(db_engine) as session:
        try:
            submenu_creating_data.menu_id = menu_id
            db_submenu = Submenu.from_orm(submenu_creating_data)
            session.add(db_submenu)

            await session.commit()
        except IntegrityError:
            return None

        await session.refresh(db_submenu)
        return db_submenu


async def update_submenu(
    submenu_id: UUID, submenu_updating_data: SubmenuUpdate
) -> Submenu | None:
    async with AsyncSession(db_engine) as session:
        db_submenu = (
            await session.exec(select(Submenu).where(Submenu.id == submenu_id))
        ).one_or_none()

        if db_submenu is None:
            return None

        await session.exec(
            update(Submenu)
            .where(Submenu.id == submenu_id)
            .values(**submenu_updating_data.dict(exclude={"id"}, exclude_unset=True))
        )

        await session.commit()
        await session.refresh(db_submenu)

        return db_submenu


async def delete_submenu(submenu_id: UUID) -> None:
    async with AsyncSession(db_engine) as session:
        await session.exec(delete(Submenu).where(Submenu.id == submenu_id))
        await session.commit()


async def read_submenu(submenu_id: UUID) -> Submenu | None:
    async with AsyncSession(db_engine) as session:
        db_submenu = await session.get(Submenu, submenu_id)
        if db_submenu is None:
            return None

        return db_submenu


async def read_all_submenus(menu_id: UUID) -> list[Submenu]:
    async with AsyncSession(db_engine) as session:
        db_submenus = (
            await session.exec(select(Submenu).where(Submenu.menu_id == menu_id))
        ).all()

        return db_submenus
