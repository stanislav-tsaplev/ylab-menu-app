from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, delete, select, update

from ...database import engine
from ..models.dish import Dish, DishCreate, DishUpdate


def create_dish(
    submenu_id: UUID, dish_creating_data: DishCreate
) -> Dish | None:
    with Session(engine) as session:
        try:
            dish_creating_data.submenu_id = submenu_id
            db_dish = Dish.from_orm(dish_creating_data)
            session.add(db_dish)

            session.commit()
        except IntegrityError:
            return None

        session.refresh(db_dish)
        return db_dish


def update_dish(dish_id: UUID, dish_updating_data: DishUpdate) -> Dish | None:
    with Session(engine) as session:
        db_dish = session.exec(
            select(Dish).where(Dish.id == dish_id)
        ).one_or_none()

        if db_dish is None:
            return None

        session.exec(
            update(Dish)
            .where(Dish.id == dish_id)
            .values(
                **dish_updating_data.dict(exclude={"id"}, exclude_unset=True)
            )
        )

        session.commit()
        session.refresh(db_dish)

        return db_dish


def delete_dish(dish_id: UUID) -> None:
    with Session(engine) as session:
        session.exec(delete(Dish).where(Dish.id == dish_id))

        session.commit()


def read_dish(dish_id: UUID) -> Dish | None:
    with Session(engine) as session:
        db_dish = session.get(Dish, dish_id)
        if db_dish is None:
            return None

        return db_dish


def read_all_dishes(submenu_id: UUID) -> list[Dish]:
    with Session(engine) as session:
        db_dishes = session.exec(
            select(Dish).where(Dish.submenu_id == submenu_id)
        ).all()

        return db_dishes
