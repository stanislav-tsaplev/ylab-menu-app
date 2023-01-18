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
            "cascade": "all, delete",   # Instruct the ORM how to track changes to local objects
            "passive_deletes": True,
        }
    )


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: str | None = None


class MenuRead(MenuBase):
    id: UUID

    submenus_count: int | None = None
    dishes_count: int | None = None
