from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import column_property
from sqlmodel import (
    SQLModel,
    Field,
    Relationship,
    ForeignKeyConstraint,
    func,
    select,
)

if TYPE_CHECKING:
    from .menu import Menu

from .dish import Dish


class Submenu(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(["menu_id"], ["menu.id"], ondelete="CASCADE"),
    )

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str | None = None

    menu_id: UUID | None = Field(default=None)
    menu: Optional["Menu"] = Relationship(back_populates="submenus")

    dishes: list["Dish"] = Relationship(
        back_populates="submenu",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "passive_deletes": True,
        },
    )


Submenu.dishes_count = column_property(
    select(func.count(Dish.id))
    .where(Submenu.id == Dish.submenu_id)
    .correlate_except(Dish)
    .scalar_subquery()
)


class SubmenuCreate(SQLModel):
    title: str
    description: str | None = None
    menu_id: UUID | None = None


class SubmenuCreated(SQLModel):
    id: UUID
    title: str
    description: str | None

    dishes_count: int = 0


class SubmenuUpdate(SQLModel):
    title: str | None = None
    description: str | None = None


class SubmenuUpdated(SQLModel):
    id: UUID
    title: str
    description: str | None

    dishes_count: int = 0


class SubmenuRead(SQLModel):
    id: UUID
    title: str
    description: str | None

    dishes_count: int = 0
