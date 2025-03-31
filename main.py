import flet as ft  # type: ignore
from db import main_db

def main(page: ft.Page):
    page.title = 'Список Покупок'
    page.theme_mode = ft.ThemeMode.DARK
    def add_product(e):
        if product_input.value.strip():
            product_id = main_db.add_products_db(product_input.value)
            product_list.controls.append(create_product_row(product_id, product_input.value, False))
            product_input.value = ""
            page.update()
    product_input = ft.TextField(
        hint_text='Добавьте товар',
        expand=True,
        dense=True,
        color=ft.colors.RED_400,
        on_submit=add_product
    )

    product_list = ft.Column(spacing=10)

    def load_products():
        product_list.controls.clear()

        for product_id, product, is_checked in main_db.get_product():
            product_list.controls.append(create_product_row(product_id, product, is_checked)) 

    def create_product_row(product_id, product_text, is_checked):
        product_field = ft.TextField(value=product_text, color=ft.colors.BLUE_400, read_only=True)
        checkbox = ft.Checkbox(value=is_checked, on_change=lambda e: toggle_product_status(product_id, checkbox.value))

        def enable_edit(e):
            product_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_product_db(product_id, product_field.value)
            product_field.read_only = True
            load_products()
            page.update()

        def delete_product(e):
            main_db.delete_product_db(product_id)
            load_products()
            page.update()

        def toggle_product_status(product_id, is_checked):
            main_db.toggle_product_status(product_id, is_checked)

        return ft.Row(
            [
                checkbox,
                product_field,
                ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_400, on_click=enable_edit),
                ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_400, on_click=save_edit),
                ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=delete_product)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    

    add_button = ft.ElevatedButton("Добавить", icon=ft.icons.ADD, on_click=add_product)

    container = ft.Container(
        content=ft.Column([
            ft.Row([product_input, add_button], alignment=ft.MainAxisAlignment.CENTER),
            product_list
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(container)
    load_products()
    page.update()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)
