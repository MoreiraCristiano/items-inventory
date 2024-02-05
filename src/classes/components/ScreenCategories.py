from flet import (
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
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.category = TextField()

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
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

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

    def generate_category_rows(self):
        """
        Description:
        Parameters:
        Return:
        """

        def change_select_state(event):
            if event.control.selected:
                event.control.selected = False
            else:
                event.control.selected = True

            self.page.update()

        for element in self.cats:
            self.categories_table.rows.append(
                DataRow(
                    [DataCell(Text(element))],
                    on_select_changed=lambda e: change_select_state(e),
                ),
            )

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def open_dlg(self, e):
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def open_dlg_modal(self, e):
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

    def build(self):
        """
        Description:
        Parameters:
        Return: Null
        """

        # obter classes do banco de dados e preencher o array/tupla
        self.cats = ['Food', 'Cleaning', 'Drinks', 'Roupa']
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
                self.categories_table,
            ],
        )

        return categories_screen
