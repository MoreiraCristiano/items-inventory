import flet as ft

from routes.routes_controller import route_change, view_pop
from classes.components.Main import Main
import sqlite3


def main(page: ft.Page):
    try:
        engine = sqlite3.connect("inventory.db")
        query_create_inventory = "CREATE TABLE inventory (id INT,item_name TEXT NOT NULL,category TEXT NOT NULL,expiration_date DATETIME NOT NULL,additional_info TEXT NOT NULL);"
        query_create_category = "CREATE TABLE category (id INT,category TEXT NOT NULL)"
        # query_create_inventory = "CREATE TABLE inventory (id INTEGER PRIMARY KEY AUTOINCREMENT,item_name TEXT NOT NULL,category TEXT NOT NULL,expiration_date DATETIME NOT NULL,additional_info TEXT NOT NULL);"
        # query_create_category = "CREATE TABLE category (id INTEGER PRIMARY KEY AUTOINCREMENT,category TEXT NOT NULL)"
        engine.execute(query_create_inventory)
        engine.execute(query_create_category)
    except Exception:
        print('fail to db')

    page.window_width = 480
    page.window_height = 800
    page.window_resizable = False
    page.window_maximizable = False
    page.title = 'Inventario'
    main_page = Main()

    page.update()

    page.on_route_change = lambda r: route_change(r, page, main_page, engine)
    page.on_view_pop = lambda v: view_pop(v, page)
    page.go(page.route)


ft.app(main)
