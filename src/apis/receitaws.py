import requests


def cnpj_lookup(companyId: str, code: str, type: int, contributor: int, cnpj: str):
    formatted_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    resp = requests.get(f"https://receitaws.com.br/v1/cnpj/{formatted_cnpj}").json()
    
    response = {
        "companyId": companyId,
        "code": code,
        "type": type,
        "contributor": contributor,

        "shortName": resp["fantasia"],
        "name": resp["nome"],
        "mainNIF": resp["cnpj"],
        "stateRegister": None,
        "zipCode": resp["cep"].replace(".", "").replace("-", "").strip(),
        "streetType": None,
        "streetName": resp["logradouro"],
        "number": resp["numero"],
        "districtType": None,
        "district": resp["bairro"],
        "countryInternalId": None,
        "stateCode": resp["uf"],
        "cityInternalId": None,
        "phoneNumber": resp["telefone"].replace("(", "").replace(")", "").replace(" ", "").replace("-", "").strip(),
        "email": resp["email"]
    }
    
    return response
