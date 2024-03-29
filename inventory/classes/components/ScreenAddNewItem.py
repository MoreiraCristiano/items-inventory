from flet import (
    Column,
    Dropdown,
    dropdown,
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


from sqlalchemy.orm import Session
from datetime import datetime
from model.InventoryItem import InventoryItem
from .ScreenCategories import ScreenCategories


class ScreenAddNewItem(UserControl):
    def __init__(self, page, database_engine):
        super().__init__()
        self.page = page
        self.engine = database_engine
        self.categories_instance = ScreenCategories(page, database_engine)
        self.item = TextField(label='Item', icon=icons.CREATE_SHARP)
        self.category = Dropdown(
            icon=icons.LABEL,
            hint_text='Category',
            options=[
                dropdown.Option(category)
                for category in self.categories_instance.get_distinct_categories()
            ],
        )
        self.extra_info = TextField(label='Extra information', icon=icons.INFO)
        self.date_picker = DatePicker(
            on_change=self.change_date,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        )

        self.btn_save = ElevatedButton(
            'Save', height=45, on_click=lambda e: self.save_item(e)
        )
        self.date_button = ElevatedButton(
            'Expiration date',
            icon=icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker.pick_date(),
            height=50,
        )

        page.overlay.append(self.date_picker)

    def set_controls_disable(self, switch):
        '''
        Description: Disable controls of the screen
        Parameters: switch: boolean, True to hide, False to show
        Return: Null
        '''
        self.btn_save.disabled = switch
        self.item.disabled = switch
        self.category.disabled = switch
        self.extra_info.disabled = switch
        self.date_button.disabled = switch

        self.page.update()

    def change_date(self, event):
        '''
        Description: Change value of the button used to set the data, to selected data
        Parameters: event: button click
        Return: Null
        '''
        self.date_button.text = self.date_picker.value.date()
        self.page.update()

    def save_item(self, event):
        '''
        Description:
        Parameters:
        Return:
        '''
        try:
            with Session(self.engine) as session:

                new_item = InventoryItem(
                    item_name=self.item.value,
                    category=self.category.value,
                    expiration_date=self.date_picker.value.date(),
                    additional_info=self.extra_info.value,
                )

                self.set_controls_disable(True)

                session.expire_on_commit = False
                session.add(new_item)
                session.commit()

                self.item.value = ''
                self.category.value = ''
                self.extra_info.value = ''
                self.date_button.text = 'Expiration date'
                self.set_controls_disable(False)

        except Exception as e:
            self.set_controls_disable(False)
            print('Algum erro ao inserir novo item. TRATAR')
            print(e)

    def build(self):
        '''
        Description: Build main view
        Parameters: Null
        Return: Null
        '''
        add_new_item_screen = View(
            '/add_new_item',
            [
                AppBar(
                    title=Text('Add new item'),
                    bgcolor='#1A1C1E',
                ),
                Column(
                    controls=[
                        self.item,
                        self.category,
                        self.extra_info,
                        self.date_button,
                    ],
                ),
                Row(
                    alignment='center',
                    controls=[self.btn_save],
                ),
            ],
        )

        return add_new_item_screen
