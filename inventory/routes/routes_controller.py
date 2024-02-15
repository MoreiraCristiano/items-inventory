import flet as ft
from classes.components.ScreenAddNewItem import ScreenAddNewItem
from classes.components.ScreenCategories import ScreenCategories
from classes.components.ScreenItems import ScreenItems


def route_change(route, page, default_view, database_engine):
    '''
    Description: Navigate between configured routes
    Parameters: route: callback | page: app page to handle | default_view: The control for route '/'
    Return: Null
    '''
    page.views.clear()
    page.views.append(ft.View('/', [default_view], vertical_alignment='center'))

    if page.route == '/add_new_item':
        screenAddNewItem = ScreenAddNewItem(page, database_engine)
        page.views.append(screenAddNewItem.build())

    if page.route == '/categories':
        screen_categories = ScreenCategories(page, database_engine)
        page.views.append(screen_categories.build())

    if page.route == '/my_items':
        screen_my_items = ScreenItems(page, database_engine)
        page.views.append(screen_my_items.build())

    page.update()


def view_pop(view, page):
    '''
    Description: Navigate between pages browser
    Parameters: view: callback mandatory parameter | page: the app page to handle
    Return: Null
    '''
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)
