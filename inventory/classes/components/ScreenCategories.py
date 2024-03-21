from flet import (
    ListView,
    Row,
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
import sqlite3


class ScreenCategories(UserControl):
    def __init__(self, page, database_engine):
        super().__init__()
        self.page = page
        self.engine = sqlite3.connect("inventory.db")

        self.categories = self.get_distinct_categories()
        self.category = TextField(autofocus=True)
        self.categories_table = DataTable(
            border_radius=10,
            sort_column_index=0,
            sort_ascending=True,
            heading_row_height=70,
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[DataColumn(Text('Category'))],
        )
        self.list_view = ListView(expand=True)
        self.list_view.controls.append(self.categories_table)

        self.dlg = AlertDialog(
            title=Text('Hello, you!'), on_dismiss=lambda e: print('Dialog dismissed!')
        )
        self.dlg_modal_new_category = AlertDialog(
            modal=True,
            title=Text('New category'),
            content=self.category,
            actions=[
                TextButton('Confirm', on_click=lambda e: self.save_category(e)),
                TextButton(
                    'Cancel',
                    on_click=lambda e: self.close_dlg(e, self.dlg_modal_new_category),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.dlg_modal_delete_category = AlertDialog(
            modal=True,
            title=Text('Delete category(s)'),
            content=Text('Delete selected categories?'),
            actions=[
                TextButton('Confirm', on_click=lambda e: self.delete_category(e)),
                TextButton(
                    'Cancel',
                    on_click=lambda e: self.close_dlg(
                        e, self.dlg_modal_delete_category
                    ),
                ),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def change_checkbox_state(self, event):
        '''
        Description: Change the checkbox selection
        Parameters: event: mouse click event
        Return: Null
        '''
        if event.control.selected:
            event.control.selected = False
        else:
            event.control.selected = True

        self.page.update()

    def generate_category_rows(self):
        '''
        Description: Use a list of categories to render a datatable with checkboxes
        Parameters: Null
        Return: Null
        '''

        for element in self.categories:
            self.categories_table.rows.append(
                DataRow(
                    [DataCell(Text(element))],
                    on_select_changed=lambda e: self.change_checkbox_state(e),
                ),
            )

    def close_dlg(self, e, modal):
        '''
        Description: Close dialog modal
        Parameters: event: mouse click event
        Return: Null
        '''
        modal.open = False
        self.page.update()

    def open_dlg(self, e):
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def open_dlg_modal(self, e, modal):
        '''
        Description: Launch a modal to set the name of the category
        Parameters: event: mouse click event
        Return: Null
        '''
        self.page.dialog = modal
        modal.open = True
        self.page.update()

    def update_category_table_values(self):
        categories_from_db = self.get_distinct_categories()
        self.categories_table.rows = []
        for category in categories_from_db:
            row = DataRow(
                [DataCell(Text(category))],
                on_select_changed=lambda e: self.change_checkbox_state(e),
            )
            self.categories_table.rows.append(row)
        self.page.update()

    def save_category(self, event):
        '''
        Description: Use the category value and save a new category to the database
        Parameters: event: mouse click event
        Return: Null | -1 if input field is empty
        '''

        if self.category.value == '':
            self.category.error_text = 'Cannot be empty value'
            self.page.update()
            self.category.error_text = ''
            return -1

        try:
            category = self.category.value
            query_save_category = f"INSERT INTO category VALUES (2, '{category}')"
            self.engine.execute(query_save_category)

            self.close_dlg(event, self.dlg_modal_new_category)
            self.category.value = ''

            self.engine.commit()

            self.update_category_table_values()

        except Exception as e:
            print(e)
            print('Falha ao criar categoria, tratar')

    def get_distinct_categories(self):
        '''
        Description: Get from database all the distinct categories
        Parameters: Null
        Return: List of categories | None
        '''

        try:
            query_get_distinct_categories = "SELECT DISTINCT category FROM category"
            categories = self.engine.execute(query_get_distinct_categories).fetchall()
            categories_list = []

            for category in categories:
                categories_list.append(category[0])

            return categories_list
        except Exception as e:
            print(e)

    def delete_category(self, event):
        categories = []

        for row in self.categories_table.rows:
            if row.selected:
                for cell in row.cells:
                    categories.append(cell.content.value)

        try:
            for category in categories:
                query_delete_category = (
                    f"DELETE FROM category WHERE category='{category}'"
                )
                self.engine.execute(query_delete_category)

            self.engine.commit()

            self.close_dlg(event, self.dlg_modal_delete_category)
            self.update_category_table_values()
        except Exception as e:
            print(e)
            print('Erro ao deletar')

        self.page.update()

    def build(self):
        '''
        Description: Build main screen after query all categories from database
        Parameters:
        Return: Null
        '''
        header = Row(
            alignment=MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ElevatedButton(
                    'New category',
                    on_click=lambda e: self.open_dlg_modal(
                        e, self.dlg_modal_new_category
                    ),
                    icon=icons.CREATE_ROUNDED,
                ),
                ElevatedButton(
                    'Delete',
                    icon=icons.DELETE,
                    on_click=lambda e: self.open_dlg_modal(
                        e, self.dlg_modal_delete_category
                    ),
                ),
            ],
        )

        self.generate_category_rows()

        categories_screen = View(
            '/categories',
            [
                AppBar(
                    title=Text('Categories'),
                    bgcolor='#1A1C1E',
                ),
                header,
                self.list_view,
            ],
        )

        return categories_screen
