import flet as ft
import datetime


class ScreenAddNewItem(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.date_picker = ft.DatePicker(
            on_change=self.change_date,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        self.date_button = ft.ElevatedButton(
            "Expiration date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker.pick_date(),
            height=50,
        )

        page.overlay.append(self.date_picker)

    def change_date(self, e):
        # armazenar valores
        print(f"Date picker changed, value is {self.date_picker.value}")

    def build(self):
        add_new_item_screen = ft.View(
            "/add_new_item",
            [
                ft.AppBar(
                    title=ft.Text("Add new item"),
                    bgcolor='#1A1C1E',
                ),
                ft.TextField(label='Item'),
                ft.TextField(label='Category'),
                ft.TextField(label='Extra information'),
                self.date_button,
                ft.Row(
                    alignment='center',
                    controls=[
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: self.page.go("/"), height=45
                        ),
                        ft.ElevatedButton("Save", height=45),
                    ],
                ),
            ],
        )

        return add_new_item_screen


def route_change(route, page, default_view):
    page.views.clear()
    page.views.append(
        ft.View(
            "/",
            [default_view],
        )
    )

    if page.route == "/add_new_item":
        screenAddNewItem = ScreenAddNewItem(page)
        page.views.append(screenAddNewItem.build())

    if page.route == "/categories":
        page.views.append(
            ft.View(
                "/categories",
                [
                    ft.AppBar(
                        title=ft.Text("Categories"),
                        bgcolor='#1A1C1E',
                    ),
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
            )
        )

    if page.route == "/my_items":
        page.views.append(
            ft.View(
                "/my_items",
                [
                    ft.AppBar(
                        title=ft.Text("My items"),
                        bgcolor='#1A1C1E',
                    ),
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                ],
            )
        )
    page.update()


def view_pop(view, page):
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)
