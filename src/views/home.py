import flet as ft
from utils.ui import show_message


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.codcoligada = str()
        self.customers_vendors = dict()
    
    def show(self):
        def add_cnpj(e):
            ...

        def remove_cnpj(cnpj):
            ...

        def start_automation(e):
            ...

        # Components
        codcoligada_input = ft.TextField()
        cnpj_input = ft.TextField()
        ie_input = ft.TextField()
        type_input = ft.Dropdown()
        add_cnpj_button = ft.Button()
        remove_cnpj_button = ft.Button()
        start_automation_button = ft.Button()
        list_of_cnpjs = ft.TextField()
        logs = ft.TextField()

        # Layout
        ...

        self.page.clean()
        self.page.add(...)
