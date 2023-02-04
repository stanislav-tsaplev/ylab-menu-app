from decimal import Decimal

from pydantic import BaseModel


class Dish(BaseModel):
    title: str
    description: str | None
    price: Decimal

    @classmethod
    def from_dict(cls, d: dict[str, str | list | dict]) -> "Catalog":
        if d is None:
            return None

        return cls(
            title=d.get("title"),
            description=d.get("description"),
            price=Decimal(str(d.get("price"))),
        )


class Submenu(BaseModel):
    title: str
    description: str | None

    dishes: list[Dish]

    @classmethod
    def from_dict(cls, d: dict[str, str | list | dict]) -> "Submenu":
        if d is None:
            return None
        return cls(
            title=d.get("title"),
            description=d.get("description"),
            dishes=[Dish.from_dict(dish_data) for dish_data in list(d["dishes"])],
        )


class Menu(BaseModel):
    title: str
    description: str | None

    submenus: list[Submenu]

    @classmethod
    def from_dict(cls, d: dict[str, str | list | dict]) -> "Menu":
        if d is None:
            return None
        return cls(
            title=d.get("title"),
            description=d.get("description"),
            submenus=[
                Submenu.from_dict(submenu_data) for submenu_data in list(d["submenus"])
            ],
        )


class Catalog(BaseModel):
    menus: list[Menu]

    @classmethod
    def from_dict(cls, d: dict[str, str | list | dict]) -> "Catalog":
        if d is None:
            return None
        return cls(menus=[Menu.from_dict(menu_data) for menu_data in list(d["menus"])])
