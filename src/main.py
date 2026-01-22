import flet as ft
import os
from views.home import HomeView


class Main:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.home_view()

    def setup_page(self):
        async def center_window():
            await self.page.window.center()
        
        self.page.title = 'CustomerVendor Automation'
        self.page.window.icon = os.path.join(os.path.dirname(__file__), "assets", "icon_windows.ico")
        self.page.run_task(center_window)
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.padding = 0
        self.page.update()

    def home_view(self):
        HomeView(self.page).show()


def main(page: ft.Page):
    Main(page)


ft.run(main, assets_dir="assets")
