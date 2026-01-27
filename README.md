# Customer Vendor Automation
Automação de cadastros de clientes e fornecedores dentro do Totvs RM usando a api do próprio RM

## Instalação (Windows)

#### 1. Clone o repositório
```
git clone https://github.com/gabriel-pagani/customer-vendor-automation.git && cd kryptex/
```

#### 2. Crie um ambiente virtual e instale as dependências
```
python -m venv venv && source venv/Scripts/activate
```
```
python -m pip install --upgrade pip && pip install -r requirements.txt
```

#### 3. Build o app
```
pyinstaller --onefile --noconsole --name "Customer Vendor" --icon src/assets/icon_windows.ico src/main.py
```

# License
See the [LICENSE](https://github.com/gabriel-pagani/customer-vendor-automation/blob/main/LICENSE) file for more details.

# Contact Information
Email: gabrielpaganidesouza@gmail.com
