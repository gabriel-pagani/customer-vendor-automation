from utils.formatter import format_name
import requests


def cnpj_lookup(companyId: str, code: str, type: int, contributor: int, cnpj: str, stateRegister: str = ""):
    formatted_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    resp = requests.get(f"https://receitaws.com.br/v1/cnpj/{formatted_cnpj}").json()
    
    response = {
        "companyId": companyId,
        "code": code,
        "type": type,
        "contributor": contributor,

        "shortName": resp["fantasia"].title().strip() if resp["fantasia"] else resp["nome"].title().strip(),
        "name": format_name(resp["nome"]),
        "mainNIF": resp["cnpj"].strip(),
        "stateRegister": stateRegister,
        "zipCode": resp["cep"].replace(".", "").replace("-", "").strip(),
        "streetType": None,
        "streetName": resp["logradouro"].title().strip(),
        "number": resp["numero"].upper().strip(),
        "districtType": None,
        "district": resp["bairro"].title().strip(),
        "stateCode": resp["uf"].upper().strip(),
        "cityInternalId": None,
        "phoneNumber": resp["telefone"].replace("(", "").replace(")", "").replace(" ", "").replace("-", "").strip(),
        "email": resp["email"].lower().strip()
    }
    
    return response
