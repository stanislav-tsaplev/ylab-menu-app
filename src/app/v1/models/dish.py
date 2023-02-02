from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from pydantic import condecimal
from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel

if TYPE_CHECKING:
    from .submenu import Submenu


class Dish(SQLModel, table=True):  # type: ignore
    __table_args__ = (
        ForeignKeyConstraint(["submenu_id"], ["submenu.id"], ondelete="CASCADE"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str | None = None
    price: condecimal(decimal_places=2) = Field(default=0)  # type: ignore

    submenu_id: UUID | None = Field(default=None)
    submenu: Optional["Submenu"] = Relationship(back_populates="dishes")


class DishCreate(SQLModel):
    title: str
    description: str | None = None
    submenu_id: UUID | None = None
    price: condecimal(decimal_places=2)  # type: ignore


class DishCreated(SQLModel):
    id: UUID
    title: str
    description: str | None
    price: str


class DishUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    price: condecimal(decimal_places=2) | None = None  # type: ignore


class DishUpdated(SQLModel):
    id: UUID
    title: str
    description: str | None
    price: str


class DishRead(SQLModel):
    id: UUID
    title: str
    description: str | None
    price: str
