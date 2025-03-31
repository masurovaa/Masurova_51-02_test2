import flet as ft
from db import main_db
from functools import partial

def main(page: ft.Page):
    page.title = 'Список покупок'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True 

    task_list = ft.Column(spacing=10)
    filter_type = "all"
    purchased_count = ft.Text("Куплено: 0")

    def load_tasks():
        task_list.controls.clear()
        completed_count = 0
        
        for task_id, task_text, quantity, completed in main_db.get_tasks(filter_type):
            if completed:
                completed_count += 1
            task_list.controls.append(create_task_row(task_id, task_text, quantity, completed))
        
        purchased_count.value = f"Куплено: {completed_count}"
        page.update()

    def create_task_row(task_id, task_text, quantity, completed):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        quantity_field = ft.TextField(value=str(quantity), width=50, dense=True, read_only=True)
        task_checkbox = ft.Checkbox(
            value=bool(completed), 
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = quantity_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task_db(task_id, task_field.value, int(quantity_field.value))
            task_field.read_only = quantity_field.read_only = True
            page.update()

        return ft.Row([
            task_checkbox,
            task_field,
            quantity_field,
            ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.YELLOW_300, on_click=enable_edit),
            ft.IconButton(ft.icons.SAVE, icon_color=ft.colors.GREEN_100, on_click=save_edit),
            ft.IconButton(ft.icons.DELETE, icon_color=ft.colors.RED_400, on_click=partial(delete_task, task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value.strip() and quantity_input.value.isdigit():
            task_id = main_db.add_task_db(task_input.value.strip(), int(quantity_input.value))
            task_list.controls.append(create_task_row(task_id, task_input.value.strip(), int(quantity_input.value), 0))
            task_input.value = ""
            quantity_input.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_tasks()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

  
  
    task_input = ft.TextField(hint_text='Название', expand=True, dense=True, on_submit=add_task)
    quantity_input = ft.TextField(hint_text='Количество', width=70, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.icons.ADD)

   
   
    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Купленные", on_click=lambda e: set_filter("completed")),
        ft.ElevatedButton("Некупленные", on_click=lambda e: set_filter("incomplete"))
    ], alignment=ft.MainAxisAlignment.CENTER)

   
   
    page.add(ft.Container(
        content=ft.Column([
            ft.Row([task_input, quantity_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            filter_buttons,
            purchased_count,
            task_list
        ], alignment=ft.MainAxisAlignment.CENTER), 
        padding=20
    ))

    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)
