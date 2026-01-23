import flet as ft
from utils.ui import show_message


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.customers_vendors = dict()
    
    def show(self):
        def update_list_of_cnpjs():
            list_of_cnpjs.controls.clear()
            for cnpj, data in self.customers_vendors.items():
                list_of_cnpjs.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.GREY_900),
                                ft.Column(
                                    controls=[
                                        ft.Text(f"Cnpj: {cnpj}", weight="bold"),
                                        ft.Text(f"Coligada: {data['codcoligada']} | Tipo: {'Cliente' if data['type'] == 'c' else 'Fornecedor'}")
                                    ], 
                                    expand=True
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Remove cnpj",
                                    on_click=lambda e, cj=cnpj: remove_cnpj_from_list(cj)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        border_radius=5
                    )
                )

            self.page.update()

        def add_cnpj_to_list(e):
            codcoligada_input.error_text = None
            cnpj_input.error = None
            type_input.error_text = None
            
            has_error = False

            if not codcoligada_input.value:
                codcoligada_input.error_text = "Required field!"
                has_error = True

            if not cnpj_input.value:
                cnpj_input.error = "Required field!"
                has_error = True

            if cnpj_input.value.strip() in self.customers_vendors:
                cnpj_input.error = "This cnpj has already been added!"
                has_error = True
            
            if not type_input.value:
                type_input.error_text = "Required field!"
                has_error = True

            if has_error:
                codcoligada_input.update()
                cnpj_input.update()
                type_input.update()
                return


            self.customers_vendors[cnpj_input.value.strip()] = {
                "codcoligada": codcoligada_input.value,
                "ie": ie_input.value.strip() if ie_input.value else "",
                "type": type_input.value
            }
            
            cnpj_input.value = ""
            ie_input.value = ""
            
            update_list_of_cnpjs()
            show_message(self.page, 1, "Cnpj added successfully!")

        def remove_cnpj_from_list(cnpj):
            if cnpj in self.customers_vendors:
                del self.customers_vendors[cnpj]
                update_list_of_cnpjs()
                show_message(self.page, 1, "Cnpj successfully removed!")

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
            icon_color=ft.Colors.GREEN,
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
