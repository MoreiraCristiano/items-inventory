from flet import (
    UserControl,
    FilledButton,
    View,
    AppBar,
    ElevatedButton,
    Text,
    icons,
    DatePicker,
    Row,
    MainAxisAlignment,
)
from datetime import datetime
from model.InventoryItem import InventoryItem
from sqlalchemy.orm import Session


class ScreenItems(UserControl):
    def __init__(self, page, database_engine):
        super().__init__()
        self.page = page
        self.engine = database_engine

        self.date_picker_from = DatePicker(
            on_change=self.change_date_btn_from,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )
        self.date_picker_to = DatePicker(
            on_change=self.change_date_btn_to,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )

        self.date_button_from = ElevatedButton(
            'From',
            icon=icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker_from.pick_date(),
            height=50,
        )
        self.date_button_to = ElevatedButton(
            'To',
            icon=icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker_to.pick_date(),
            height=50,
        )

        self.search_btn = FilledButton(
            'Search',
            icon=icons.SEARCH,
            on_click=lambda e: self.query_items_by_date_interval(e),
        )

        page.overlay.append(self.date_picker_from)
        page.overlay.append(self.date_picker_to)

    def change_date_btn_from(self, event):
        '''
        Description: Change value of the button used to set the data, to selected data
        Parameters: event: button click
        Return: Null
        '''

        self.date_button_from.text = self.date_picker_from.value.date()
        self.page.update()

    def change_date_btn_to(self, event):
        '''
        Description: Change value of the button used to set the data, to selected data
        Parameters: event: button click
        Return: Null
        '''
        self.date_button_to.text = self.date_picker_to.value.date()
        self.page.update()

    def query_items_by_date_interval(self, event):
        # Tratar tipo do dado para ser somente a data e nao text do btn cru
        try:
            date_from = self.date_button_from.text
            date_to = self.date_button_to.text

            with Session(self.engine) as session:
                query = session.query(InventoryItem).filter(
                    InventoryItem.expiration_date.between(date_from, date_to)
                )

                if query.count() != 0:
                    for element in query:
                        print(element)
                else:
                    print('sem dados nessa data')
        except Exception as e:
            print('Falha ao buscar dados', e)

    def build(self):
        screen = View(
            '/my_items',
            [
                AppBar(
                    title=Text('My items'),
                    bgcolor='#1A1C1E',
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        self.date_button_from,
                        self.date_button_to,
                    ],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[self.search_btn],
                ),
            ],
        )

        return screen
