from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from model.InventoryItem import Category
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

        self.categories = self.get_distinct_categories()
        self.category = TextField(autofocus=True)
        self.categories_table = DataTable(
            width=700,
            border_radius=10,
            sort_column_index=0,
            sort_ascending=True,
            heading_row_height=70,
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[DataColumn(Text('Category'))],
        )
        self.list_view = ListView(expand=1, spacing=10, padding=20)
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
        Return: Null
        '''
        with Session(self.engine) as session:
            try:
                category = Category(category=self.category.value)

                session.expire_on_commit = False
                session.add(category)
                session.commit()

                self.close_dlg(event, self.dlg_modal_new_category)
                self.category.value = ''

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
        with Session(self.engine) as session:
            try:
                stmt = select(Category.category)
                categories = list(session.scalars(stmt))
                return categories
            except Exception as e:
                print(e)

    def delete_category(self, event):

        # Obter os valores da data table que estiverem selecionados
        # Modal: Deletar selecionados ? Yes / No
        # If yes delete the selected
        # dlg_modal_delete_category
        print('deletando as categorias selecionadas . . .')

        categories = ['teste', 'teste2', 'teste3']

        try:
            with Session(self.engine) as session:
                session.expire_on_commit = False

                for category in categories:
                    stmt = delete(Category).where(Category.category == category)
                    session.execute(stmt)

                session.commit()

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
        self.generate_category_rows()

        categories_screen = View(
            '/categories',
            [
                AppBar(
                    title=Text('Categories'),
                    bgcolor='#1A1C1E',
                ),
                ElevatedButton('Home', on_click=lambda _: self.page.go('/')),
                ElevatedButton(
                    'New category',
                    on_click=lambda e: self.open_dlg_modal(
                        e, self.dlg_modal_new_category
                    ),
                ),
                ElevatedButton(
                    'Delete',
                    icon=icons.DELETE,
                    on_click=lambda e: self.open_dlg_modal(
                        e, self.dlg_modal_delete_category
                    ),
                ),
                self.list_view,
            ],
        )

        return categories_screen
