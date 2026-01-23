import flet as ft
import time
from utils.ui import show_message
from utils.validator import is_valid_cnpj
from apis.receitaws import cnpj_lookup
from apis.customer_vendor import create_new_customer_vendor
from database.connection import execute_query


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
                                        ft.Text(f"Cnpj: {cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}", weight="bold"),
                                        ft.Text(f"Coligada: {"Sinasc" if data["codcoligada"] == "5" else ("ICD" if data["codcoligada"] == "6" else "BRS")} | Tipo: {"Cliente" if data["type"] == "c" else "Fornecedor"} | IE: {data["ie"]}" if data["ie"] else f"Coligada: {"Sinasc" if data["codcoligada"] == "5" else ("ICD" if data["codcoligada"] == "6" else "BRS")} | Tipo: {"Cliente" if data["type"] == "c" else "Fornecedor"}")
                                    ], 
                                    expand=True
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Remover cnpj",
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
                codcoligada_input.error_text = "Campo obrigatório!"
                has_error = True

            if not cnpj_input.value:
                cnpj_input.error = "Campo obrigatório!"
                has_error = True

            if cnpj_input.value in self.customers_vendors:
                cnpj_input.error = "Esse cnpj já foi adicionado!"
                has_error = True

            if cnpj_input.value and not is_valid_cnpj(cnpj_input.value):
                cnpj_input.error = "Cnpj inválido!"
                has_error = True
            
            if not type_input.value:
                type_input.error_text = "Campo obrigatório!"
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
            show_message(self.page, 1, "Cnpj adicionado com sucesso!")

        def remove_cnpj_from_list(cnpj):
            if cnpj in self.customers_vendors:
                del self.customers_vendors[cnpj]
                update_list_of_cnpjs()
                show_message(self.page, 1, "Cnpj removido com sucesso!")

        async def run_automation_tesk():
            codcoligada_input.disabled = True
            cnpj_input.disabled = True
            ie_input.disabled = True
            type_input.disabled = True
            add_cnpj_button.disabled = True
            add_cnpj_button.tooltip = "Automação em execução!"
            start_automation_button.disabled = True
            start_automation_button.tooltip = "Automação em execução!"

            for container in list_of_cnpjs.controls:
                container.content.controls[2].disabled = True
                container.content.controls[2].tooltip = "Automação em execução!"
            
            self.page.update()

            len_customers_vendors = len(self.customers_vendors)
            for cnpj, infos in self.customers_vendors.items():
                try:
                    data = execute_query("""
                        SELECT
                            'F' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' AND CODCOLIGADA in (1,5,6) ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_FOR,
                            'C' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' AND CODCOLIGADA in (1,5,6) ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_CLI
                    """)
                    codcfo = data[0][1] if infos["type"].lower() == "c" else data[0][0]
                    
                    resp = cnpj_lookup(codcoligada=infos["codcoligada"], codcfo=codcfo, cnpj=cnpj, ie=infos["ie"])

                    create_new_customer_vendor(
                        companyId=resp["companyId"],
                        code=resp["code"],
                        shortName=resp["shortName"],
                        name=resp["name"],
                        type=resp["type"],
                        mainNIF=resp["mainNIF"],
                        stateRegister=resp["stateRegister"],
                        zipCode=resp["zipCode"],
                        streetType=resp["streetType"],
                        streetName=resp["streetName"],
                        number=resp["number"],
                        districtType=resp["districtType"],
                        district=resp["district"],
                        stateCode=resp["stateCode"],
                        cityInternalId=resp["cityInternalId"],
                        phoneNumber=resp["phoneNumber"],
                        email=resp["email"],
                        contributor=resp["contributor"]
                    )

                    if len_customers_vendors > 3:
                        time.sleep(20)

                except Exception as e:
                    print(f"exception: {e}")

            codcoligada_input.disabled = False
            cnpj_input.disabled = False
            ie_input.disabled = False
            type_input.disabled = False
            add_cnpj_button.disabled = False
            add_cnpj_button.tooltip = "Adicionar cnpj"
            start_automation_button.disabled = False
            start_automation_button.tooltip = None

            for container in list_of_cnpjs.controls:
                container.content.controls[2].disabled = False
                container.content.controls[2].tooltip = "Remover cnpj"

            self.customers_vendors = dict()
            update_list_of_cnpjs()
            
            self.page.update()
            show_message(self.page, 1, "Automação finalizada!")
        
        def start_automation(e):
            if not self.customers_vendors:
                show_message(self.page, 2, "A lista de cnpjs está vazia!")
                return
            
            self.page.run_task(run_automation_tesk)


        # Components
        codcoligada_input = ft.Dropdown(
            label="Coligada",
            width=200,
            options=[
                ft.dropdown.Option("5", "Sinasc"),
                ft.dropdown.Option("6", "ICD"),
                ft.dropdown.Option("1", "BRS"),
            ]
        )

        cnpj_input = ft.TextField(
            label="Cnpj",
            expand=True,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_submit=add_cnpj_to_list,
        )

        ie_input = ft.TextField(
            label="IE",
            expand=True,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_submit=add_cnpj_to_list,
        )

        type_input = ft.Dropdown(
            label="Tipo",
            width=200,
            options=[
                ft.dropdown.Option("c", "Cliente"),
                ft.dropdown.Option("f", "Fornecedor"),
            ]
        )

        add_cnpj_button = ft.IconButton(
            icon=ft.Icons.ADD_CIRCLE,
            icon_color=ft.Colors.GREEN,
            icon_size=40,
            tooltip="Adicionar cnpj",
            on_click=add_cnpj_to_list,
        )

        start_automation_button = ft.Button(
            content=ft.Text("Iniciar automação"),
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
                ft.Text("Clientes/Fornecedores:", size=16, weight="bold"),
                ft.Container(
                    content=list_of_cnpjs,
                    expand=True,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=5
                ),
                ft.Text("Logs:", size=16, weight="bold"),
                ft.Container(
                    content=logs,
                    height=150,
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
