from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship, ForeignKeyConstraint
from pydantic import condecimal

if TYPE_CHECKING:
    from .submenu import Submenu


class DishBase(SQLModel):
    title: str
    description: str | None = None


class Dish(DishBase, table=True):
    __table_args__ = (
        ForeignKeyConstraint(["submenu_id"], ["submenu.id"], ondelete="CASCADE"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    price: condecimal(decimal_places=2) = Field(default=0)

    submenu_id: UUID | None = Field(default=None)
    submenu: Optional["Submenu"] = Relationship(back_populates="dishes")


class DishCreate(DishBase):
    submenu_id: UUID | None = None
    price: condecimal(decimal_places=2)


class DishUpdate(DishBase):
    title: str | None = None
    price: condecimal(decimal_places=2) | None = None


class DishRead(DishBase):
    id: UUID
    price: str
