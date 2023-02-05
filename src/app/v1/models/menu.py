from uuid import UUID, uuid4

from sqlalchemy.orm import column_property
from sqlmodel import SQLModel, Field, Relationship, select, func

from .dish import Dish
from .submenu import Submenu


class Menu(SQLModel, table=True):  # type: ignore[call-arg]
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str | None = None

    submenus: list["Submenu"] = Relationship(
        back_populates="menu",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "passive_deletes": True,
        },
    )


Menu.submenus_count = column_property(
    select(func.count(Submenu.id))
    .where(Menu.id == Submenu.menu_id)
    .correlate_except(Submenu)
    .scalar_subquery()
)

Menu.dishes_count = column_property(
    select(func.count(Dish.id))
    .join(Submenu)
    .where(Menu.id == Submenu.menu_id and Submenu.id == Dish.submenu_id)
    .correlate_except(Dish)
    .scalar_subquery()
)


class MenuCreate(SQLModel):
    title: str
    description: str | None = None


class MenuCreated(SQLModel):
    id: UUID
    title: str
    description: str | None

    submenus_count: int = 0
    dishes_count: int = 0


class MenuUpdate(SQLModel):
    title: str | None = None
    description: str | None = None


class MenuUpdated(SQLModel):
    id: UUID
    title: str
    description: str | None

    submenus_count: int = 0
    dishes_count: int = 0


class MenuRead(SQLModel):
    id: UUID
    title: str
    description: str | None

    submenus_count: int = 0
    dishes_count: int = 0
