from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .submenu import Submenu


class MenuBase(SQLModel):
    title: str
    description: str | None = None


class Menu(MenuBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    submenus: list["Submenu"] = Relationship(
        back_populates="menu",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "passive_deletes": True,
        }
    )


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: str | None = None


class MenuRead(MenuBase):
    id: UUID

    submenus_count: int = 0
    dishes_count: int = 0
