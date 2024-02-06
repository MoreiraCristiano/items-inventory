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


from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from model.InventoryItem import InventoryItem


class ScreenAddNewItem(UserControl):
    def __init__(self, page, database_engine):
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
        self.engine = database_engine
        page.overlay.append(self.date_picker)

    def change_date(self, event):
        # armazenar valores
        self.date_button.text = self.date_picker.value.date()
        self.page.update()

    def save_item(self, event):
        """
        Description:
        Parameters:
        Return:
        """
        try:
            with Session(self.engine) as session:
                new_item = InventoryItem(
                    item_name=self.item.value,
                    category=self.category.value,
                    expiration_date=self.date_picker.value.date(),
                    additional_info=self.extra_info.value,
                )
                session.expire_on_commit = False
                session.add(new_item)
                session.commit()

                self.item.value = ''
                self.category.value = ''
                self.extra_info.value = ''
                self.page.update()
        except Exception:
            print('Algum erro ao inserir novo item. TRATAR')

    def build(self):
        """
        Description:
        Parameters:
        Return:
        """
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
