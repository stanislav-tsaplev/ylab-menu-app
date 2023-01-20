from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .submenu import Submenu


class Menu(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str | None = None

    submenus: list["Submenu"] = Relationship(
        back_populates="menu",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "passive_deletes": True,
        }
    )


class MenuCreate(SQLModel):
    title: str
    description: str | None = None


class MenuCreated(SQLModel):
    id: UUID
    title: str
    description: str | None


class MenuUpdate(SQLModel):
    title: str | None = None
    description: str | None = None


class MenuUpdated(SQLModel):
    id: UUID
    title: str
    description: str | None


class MenuRead(SQLModel):
    id: UUID
    title: str
    description: str | None

    submenus_count: int = 0
    dishes_count: int = 0
