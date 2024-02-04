import flet as ft
from classes.components.ScreenAddNewItem import ScreenAddNewItem


def route_change(route, page, default_view):
    page.views.clear()
    page.views.append(ft.View("/", [default_view], vertical_alignment='center'))

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
