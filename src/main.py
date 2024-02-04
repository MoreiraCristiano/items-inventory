import flet as ft

from routes.routes_controller import route_change, view_pop

BUTTONS_WIDTH = 350
BUTTONS_HEIGHT = 50
APP_TITLE = 'INVENTARIO'


class Main(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        main_page = ft.Column(
            horizontal_alignment='center',
            controls=[
                ft.Row(
                    controls=[ft.Text(APP_TITLE, size=25, weight=ft.FontWeight.W_500)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            'Add new item',
                            width=BUTTONS_WIDTH,
                            height=BUTTONS_HEIGHT,
                            on_click=lambda e: e.page.go("/add_new_item"),
                        ),
                        ft.ElevatedButton(
                            'My items',
                            width=BUTTONS_WIDTH,
                            height=BUTTONS_HEIGHT,
                            on_click=lambda e: e.page.go("/my_items"),
                        ),
                        ft.ElevatedButton(
                            'Categories',
                            width=BUTTONS_WIDTH,
                            height=BUTTONS_HEIGHT,
                            on_click=lambda e: e.page.go("/categories"),
                        ),
                    ],
                ),
            ],
        )

        return main_page


def main(page: ft.Page):
    page.window_width = 480
    page.window_height = 800
    page.window_resizable = False
    page.window_maximizable = False
    # page.vertical_alignment = 'center'
    # page.horizontal_alignment = 'center'
    page.title = "Routes Example"

    main_page = Main()

    page.on_route_change = lambda r: route_change(r, page, main_page)
    page.on_view_pop = lambda v: view_pop(v, page)
    page.go(page.route)


ft.app(main)
