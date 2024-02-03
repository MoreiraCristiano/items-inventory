import flet as ft


class ScreenAddNewItem(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

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
                ft.TextField(label='Expiration'),
                ft.TextField(label='Extra information'),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Go Home", on_click=lambda _: self.page.go("/")
                        ),
                        ft.ElevatedButton("Save"),
                    ]
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
