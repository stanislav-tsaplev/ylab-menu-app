from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import select, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import db_engine
from ..models.dish import Dish, DishCreate, DishUpdate


async def create_dish(submenu_id: UUID, dish_creating_data: DishCreate) -> Dish | None:
    async with AsyncSession(db_engine) as session:
        try:
            dish_creating_data.submenu_id = submenu_id
            db_dish = Dish.from_orm(dish_creating_data)
            session.add(db_dish)

            await session.commit()
        except IntegrityError:
            return None

        await session.refresh(db_dish)
        return db_dish


async def update_dish(dish_id: UUID, dish_updating_data: DishUpdate) -> Dish | None:
    async with AsyncSession(db_engine) as session:
        db_dish = (
            await session.exec(select(Dish).where(Dish.id == dish_id))
        ).one_or_none()

        if db_dish is None:
            return None

        await session.exec(
            update(Dish)
            .where(Dish.id == dish_id)
            .values(**dish_updating_data.dict(exclude={"id"}, exclude_unset=True))
        )

        await session.commit()
        await session.refresh(db_dish)

        return db_dish


async def delete_dish(dish_id: UUID) -> None:
    async with AsyncSession(db_engine) as session:
        await session.exec(delete(Dish).where(Dish.id == dish_id))

        await session.commit()


async def read_dish(dish_id: UUID) -> Dish | None:
    async with AsyncSession(db_engine) as session:
        db_dish = await session.get(Dish, dish_id)
        if db_dish is None:
            return None

        return db_dish


async def read_all_dishes(submenu_id: UUID) -> list[Dish]:
    async with AsyncSession(db_engine) as session:
        db_dishes = (
            await session.exec(select(Dish).where(Dish.submenu_id == submenu_id))
        ).all()

        return db_dishes
