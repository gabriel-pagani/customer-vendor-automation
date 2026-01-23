import flet as ft
import asyncio
from utils.ui import show_message
from apis.receitaws import cnpj_lookup
from apis.customer_vendor import create_new_customer_vendor


class HomeView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.customers_vendors = dict()  # Armazena os dados: {cnpj: {dados...}}
    
    def show(self):
        # Componentes de Lista e Logs definidos antecipadamente para serem usados nas funções
        list_of_cnpjs = ft.ListView(expand=True, spacing=10)
        logs = ft.ListView(expand=True, spacing=5, auto_scroll=True)

        def update_list():
            list_of_cnpjs.controls.clear()
            for cnpj, data in self.customers_vendors.items():
                list_of_cnpjs.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.BLUE),
                            ft.Column([
                                ft.Text(f"Código: {data['code']} | CNPJ: {cnpj}", weight="bold"),
                                ft.Text(f"Coligada: {data['codcoligada']} | Tipo: {'Cliente' if data['type'] == 'c' else 'Fornecedor'}")
                            ], expand=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Remover",
                                on_click=lambda e, c=cnpj: remove_cnpj(c)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5
                    )
                )
            self.page.update()

        def add_cnpj(e):
            if not all([codcoligada_input.value, cnpj_input.value, type_input.value]):
                show_message(self.page, 2, "Por favor, preencha todos os campos.")
                return

            cnpj_val = cnpj_input.value.strip()
            
            if cnpj_val in self.customers_vendors:
                show_message(self.page, 2, "Este CNPJ já foi adicionado.")
                return

            self.customers_vendors[cnpj_val] = {
                "codcoligada": codcoligada_input.value,
                "ie": ie_input.value.strip() if ie_input.value else "",
                "type": type_input.value
            }
            
            # Limpa campos opcionais ou de texto simples para facilitar nova entrada
            cnpj_input.value = ""
            ie_input.value = ""
            # code_input.value = "" # Opcional: limpar ou manter o código para sequencia
            cnpj_input.focus()
            
            update_list()
            show_message(self.page, 1, "CNPJ adicionado com sucesso!")

        def remove_cnpj(cnpj):
            if cnpj in self.customers_vendors:
                del self.customers_vendors[cnpj]
                update_list()
                show_message(self.page, 4, "Item removido.")

        async def run_automation_task():
            if not self.customers_vendors:
                show_message(self.page, 2, "A lista está vazia.")
                return

            start_automation_button.disabled = True
            self.page.update()

            logs.controls.append(ft.Text("Iniciando automação...", color=ft.Colors.BLUE))
            self.page.update()

            for cnpj, data in self.customers_vendors.items():
                try:
                    logs.controls.append(ft.Text(f"Processando CNPJ: {cnpj}...", italic=True))
                    self.page.update()

                    # 1. Consulta ReceitaWS (Executado em thread para não travar UI)
                    api_data = await asyncio.to_thread(
                        cnpj_lookup, 
                        codcoligada=data['codcoligada'],
                        codcfo=data['code'],
                        cnpj=cnpj,
                        ie=data['ie']
                    )

                    # 2. Cria Cliente/Fornecedor no ERP
                    await asyncio.to_thread(
                        create_new_customer_vendor, 
                        **api_data
                    )

                    logs.controls.append(ft.Text(f"✅ Sucesso: {data['code']} - {api_data['name']}", color=ft.Colors.GREEN))

                except Exception as ex:
                    logs.controls.append(ft.Text(f"❌ Erro no CNPJ {cnpj}: {str(ex)}", color=ft.Colors.RED))
                
                self.page.update()

            logs.controls.append(ft.Text("Automação finalizada.", weight="bold"))
            start_automation_button.disabled = False
            self.page.update()

        def start_automation(e):
            self.page.run_task(run_automation_task)

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
            on_submit=add_cnpj,
        )

        ie_input = ft.TextField(
            label="IE",
            expand=True,
            on_submit=add_cnpj,
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
            on_click=add_cnpj,
        )

        start_automation_button = ft.Button(
            content=ft.Text("Start automation"),
            height=50,
            bgcolor=ft.Colors.GREY_900,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=start_automation, # Corrigido: chama a função de automação
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
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10
                ),
                ft.Divider(),
                ft.Text("Lista de Processamento:", size=16, weight="bold"),
                ft.Container(
                    content=list_of_cnpjs,
                    expand=True, # Ocupa o espaço disponível
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=5
                ),
                ft.Divider(),
                ft.Text("Logs:", size=16, weight="bold"),
                ft.Container(
                    content=logs,
                    height=150, # Altura fixa para os logs
                    bgcolor=ft.Colors.BLACK_12,
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
