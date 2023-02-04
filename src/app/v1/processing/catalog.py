import xlsxwriter

from ..models.catalog import Catalog


def generate_xls_file(catalog_data: Catalog, xls_filename: str):
    workbook = xlsxwriter.Workbook(xls_filename)
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({"align": "center", "bold": True})
    currency_format = workbook.add_format({"num_format": "# ##0,00 ₽;-# ##0,00 ₽"})

    worksheet.set_column(0, 0, width=6)
    worksheet.set_column(1, 1, width=50)
    worksheet.set_column(2, 2, width=75)
    worksheet.set_column(3, 3, width=10, cell_format=currency_format)

    table_data: list[tuple] = []
    for menu_num, menu_data in enumerate(catalog_data.menus, start=1):
        table_data.append((f"{menu_num}", menu_data.title, menu_data.description))
        for submenu_num, submenu_data in enumerate(menu_data.submenus, start=1):
            table_data.append(
                (
                    f"{menu_num}.{submenu_num}",
                    submenu_data.title,
                    submenu_data.description,
                )
            )
            for dish_num, dish_data in enumerate(submenu_data.dishes, start=1):
                table_data.append(
                    (
                        f"{menu_num}.{submenu_num}.{dish_num}",
                        dish_data.title,
                        dish_data.description,
                        dish_data.price,
                    )
                )
            table_data.append(())

    worksheet.add_table(
        first_row=0,
        first_col=0,
        last_row=len(table_data),
        last_col=3,
        options={
            "data": table_data,
            "columns": [
                {"header": "#", "header_format": header_format},
                {"header": "Наименование", "header_format": header_format},
                {"header": "Описание", "header_format": header_format},
                {"header": "Цена", "header_format": header_format},
            ],
        },
    )

    workbook.close()
