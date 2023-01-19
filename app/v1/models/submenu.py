from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship, ForeignKeyConstraint

if TYPE_CHECKING:
    from .menu import Menu
    from .dish import Dish


class SubmenuBase(SQLModel):
    title: str
    description: str | None = None


class Submenu(SubmenuBase, table=True):
    __table_args__ = (
        ForeignKeyConstraint(["menu_id"], ["menu.id"], ondelete="CASCADE"),
    )

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    menu_id: UUID | None = Field(default=None)
    menu: Optional["Menu"] = Relationship(back_populates="submenus")

    dishes: list["Dish"] = Relationship(
        back_populates="submenu",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "passive_deletes": True,
        }
    )

class SubmenuCreate(SubmenuBase):
    menu_id: UUID | None = None


class SubmenuUpdate(SubmenuBase):
    title: str | None = None


class SubmenuRead(SubmenuBase):
    id: UUID
    menu_id: UUID

    dishes_count: int | None = None
