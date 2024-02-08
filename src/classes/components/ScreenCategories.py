from sqlalchemy import select
from sqlalchemy.orm import Session
from model.InventoryItem import InventoryItem
from flet import (
    ListView,
    UserControl,
    View,
    AppBar,
    ElevatedButton,
    Text,
    AlertDialog,
    MainAxisAlignment,
    TextButton,
    TextField,
    DataCell,
    DataColumn,
    DataTable,
    DataRow,
    icons,
)


class ScreenCategories(UserControl):
    def __init__(self, page, database_engine):
        super().__init__()
        self.page = page
        self.engine = database_engine

        self.categories = []
        self.get_distinct_categories()
        self.category = TextField()
        self.categories_table = DataTable(
            width=700,
            border_radius=10,
            sort_column_index=0,
            sort_ascending=True,
            heading_row_height=70,
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[DataColumn(Text("Category"))],
        )
        self.list_view = ListView(expand=1, spacing=10, padding=20)
        self.list_view.controls.append(self.categories_table)

        self.dlg = AlertDialog(
            title=Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
        )
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("New category"),
            content=self.category,
            actions=[
                TextButton("Confirm", on_click=lambda e: self.save_category(e)),
                TextButton("Cancel", on_click=lambda e: self.close_dlg(e)),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def generate_category_rows(self):
        """
        Description: Use a list of categories to render a datatable with checkboxes
        Parameters: Null
        Return: Null
        """

        def change_select_state(event):
            if event.control.selected:
                event.control.selected = False
            else:
                event.control.selected = True

            self.page.update()

        for element in self.categories:
            self.categories_table.rows.append(
                DataRow(
                    [DataCell(Text(element))],
                    on_select_changed=lambda e: change_select_state(e),
                ),
            )

    def close_dlg(self, e):
        """
        Description: Close dialog modal
        Parameters: event: mouse click event
        Return: Null
        """
        self.dlg_modal.open = False
        self.page.update()

    def open_dlg(self, e):
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def open_dlg_modal(self, e):
        """
        Description: Launch a modal to set the name of the category
        Parameters: event: mouse click event
        Return: Null
        """
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def save_category(self, event):
        """
        Description: Use the category value and save a new category to the database
        Parameters: event: mouse click event
        Return: Null
        """
        self.close_dlg(event)
        print(self.category.value)
        self.category.value = ''

    def get_distinct_categories(self):
        with Session(self.engine) as session:
            try:
                stmt = select(InventoryItem.category)
                self.categories = list(session.scalars(stmt))
            except Exception as e:
                print(e)

    def build(self):
        """
        Description: Build main screen after query all categories from database
        Parameters:
        Return: Null
        """
        self.generate_category_rows()

        categories_screen = View(
            "/categories",
            [
                AppBar(
                    title=Text("Categories"),
                    bgcolor='#1A1C1E',
                ),
                ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
                ElevatedButton("New category", on_click=self.open_dlg_modal),
                ElevatedButton('Delete', icon=icons.DELETE),
                self.list_view,
            ],
        )

        return categories_screen
