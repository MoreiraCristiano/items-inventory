from flet import (
    UserControl,
    Text,
    Column,
    Row,
    ElevatedButton,
    MainAxisAlignment,
    FontWeight,
)

BUTTONS_WIDTH = 350
BUTTONS_HEIGHT = 50
APP_TITLE = 'INVENTARIO'


class Main(UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        '''
        Description: Render main menu component
        Parameters: Null
        Return: A control component to render
        '''
        main_page = Column(
            horizontal_alignment='center',
            controls=[
                Row(
                    controls=[Text(APP_TITLE, size=25, weight=FontWeight.W_500)],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Column(
                    controls=[
                        ElevatedButton(
                            'Add new item',
                            width=BUTTONS_WIDTH,
                            height=BUTTONS_HEIGHT,
                            on_click=lambda e: e.page.go('/add_new_item'),
                        ),
                        ElevatedButton(
                            'My items',
                            width=BUTTONS_WIDTH,
                            height=BUTTONS_HEIGHT,
                            on_click=lambda e: e.page.go('/my_items'),
                        ),
                        ElevatedButton(
                            'Categories',
                            width=BUTTONS_WIDTH,
                            height=BUTTONS_HEIGHT,
                            on_click=lambda e: e.page.go('/categories'),
                        ),
                    ],
                ),
            ],
        )

        return main_page
