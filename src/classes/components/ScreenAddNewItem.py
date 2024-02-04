from flet import (
    UserControl,
    TextField,
    DatePicker,
    icons,
    View,
    AppBar,
    Text,
    Row,
    ElevatedButton,
)

from datetime import datetime


class ScreenAddNewItem(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.item = TextField(label='Item')
        self.category = TextField(label='Category')
        self.extra_info = TextField(label='Extra information')

        self.date_picker = DatePicker(
            on_change=self.change_date,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )

        self.date_button = ElevatedButton(
            "Expiration date",
            icon=icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker.pick_date(),
            height=50,
        )

        page.overlay.append(self.date_picker)

    def change_date(self, event):
        # armazenar valores
        self.date_button.text = self.date_picker.value.date()
        self.page.update()

    def save_item(self, event):
        # Checar e tratar itens vazios
        print(self.item.value)
        print(self.category.value)
        print(self.extra_info.value)
        print(self.date_picker.value.date())

    def build(self):
        add_new_item_screen = View(
            "/add_new_item",
            [
                AppBar(
                    title=Text("Add new item"),
                    bgcolor='#1A1C1E',
                ),
                self.item,
                self.category,
                self.extra_info,
                self.date_button,
                Row(
                    alignment='center',
                    controls=[
                        ElevatedButton(
                            "Go Home", on_click=lambda _: self.page.go("/"), height=45
                        ),
                        ElevatedButton(
                            "Save", height=45, on_click=lambda e: self.save_item(e)
                        ),
                    ],
                ),
            ],
        )

        return add_new_item_screen
