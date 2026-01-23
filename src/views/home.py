import flet as ft
from utils.ui import show_message


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.customers_vendors = dict()
    
    def show(self):
        def update_list_of_cnpjs(e):
            ...

        def add_cnpj_to_list(e):
            ...

        def remove_cnpj_from_list(cnpj):
            ...

        def start_automation(e):
            ...

        # Components
        codcoligada_input = ft.Dropdown(
            label="Affiliate",
            width=150,
            options=[
                ft.dropdown.Option("5", "Sinasc"),
                ft.dropdown.Option("6", "ICD"),
                ft.dropdown.Option("1", "BRS"),
            ]
        )

        cnpj_input = ft.TextField(
            label="Cnpj",
            expand=True,
            on_submit=add_cnpj_to_list,
        )

        ie_input = ft.TextField(
            label="IE",
            expand=True,
            on_submit=add_cnpj_to_list,
        )

        type_input = ft.Dropdown(
            label="Type",
            width=150,
            options=[
                ft.dropdown.Option("c", "Customer"),
                ft.dropdown.Option("f", "Vendor"),
            ]
        )

        add_cnpj_button = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=ft.Colors.GREY_900,
            icon_size=40,
            tooltip="Add cnpj",
            on_click=add_cnpj_to_list,
        )

        remove_cnpj_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_size=30,
            tooltip="Remove cnpj",
            on_click=remove_cnpj_from_list,
        )

        start_automation_button = ft.Button(
            content=ft.Text("Start automation"),
            height=50,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=start_automation,
        )

        list_of_cnpjs = ft.ListView(
            expand=True, 
            spacing=10
        )
        
        logs = ft.ListView(
            expand=True, 
            spacing=5, 
            auto_scroll=True
        )

        
        # Layout
        cnpj_form = ft.Row(
            controls=[
                codcoligada_input,
                cnpj_input,
                ie_input,
                type_input,
                add_cnpj_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        column = ft.Column(
            controls=[
                ft.Container(
                    content=cnpj_form,
                    padding=10,
                    bgcolor=ft.Colors.TRANSPARENT,
                    border_radius=10
                ),
                ft.Text("Customers/Vendors:", size=16, weight="bold"),
                ft.Container(
                    content=list_of_cnpjs,
                    expand=True,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=5
                ),
                ft.Divider(),
                ft.Text("Logs:", size=16, weight="bold"),
                ft.Container(
                    content=logs,
                    expand=True,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10
                ),
                ft.Container(
                    content=start_automation_button,
                    padding=ft.Padding.only(top=10)
                ),
            ],
            expand=True
        )

        container = ft.Container(
            content=column,
            padding=20,
            expand=True
        )

        self.page.clean()
        self.page.add(container)
