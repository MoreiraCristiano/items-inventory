from flet import UserControl, View, AppBar, ElevatedButton, Text


class ScreenItems(UserControl):
    def __init__(self, page, database_engine):
        super().__init__()
        self.page = page
        self.engine = database_engine

    def build(self):
        screen = View(
            '/my_items',
            [
                AppBar(
                    title=Text('My items'),
                    bgcolor='#1A1C1E',
                ),
                ElevatedButton('Go Home', on_click=lambda _: self.page.go('/')),
            ],
        )

        return screen
