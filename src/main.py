import flet as ft

from routes.routes_controller import route_change, view_pop
from classes.components.Main import Main
from model.InventoryItem import Base
from sqlalchemy import create_engine


engine = create_engine('sqlite:///inventory.sqlite3', echo=False)
Base.metadata.create_all(engine)


def main(page: ft.Page):
    page.window_width = 480
    page.window_height = 800
    page.window_resizable = False
    page.window_maximizable = False
    page.title = "Routes Example"
    main_page = Main()

    page.update()

    page.on_route_change = lambda r: route_change(r, page, main_page, engine)
    page.on_view_pop = lambda v: view_pop(v, page)
    page.go(page.route)


ft.app(main)
