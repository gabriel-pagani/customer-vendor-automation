import requests


def cnpj_lookup(cnpj: str):
    formatted_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    response = requests.get(f"https://receitaws.com.br/v1/cnpj/{formatted_cnpj}")
    return response.json()
