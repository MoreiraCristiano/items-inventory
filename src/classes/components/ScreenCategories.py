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
        categories_screen = View(
            "/categories",
            [
                AppBar(
                    title=Text("Categories"),
                    bgcolor='#1A1C1E',
                ),
                ElevatedButton("Home", on_click=lambda _: self.page.go("/")),
                ElevatedButton("New category", on_click=self.open_dlg_modal),
            ],
        )

        return categories_screen
