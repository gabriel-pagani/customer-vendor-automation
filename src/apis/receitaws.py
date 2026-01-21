from utils.formatter import format_name, suffix_remover, format_zipcode, format_street, format_district, format_phone
import requests


def cnpj_lookup(codcoligada: str, codcfo: str, cnpj: str, ie: str = ""):
    formatted_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    resp = requests.get(f"https://receitaws.com.br/v1/cnpj/{formatted_cnpj}").json()
    
    response = {
        "companyId": codcoligada,
        "code": codcfo,
        "type": 3 if codcfo.upper().startswith('C') else 2,  # Conferir os tipos de cadastro
        "contributor": 2 if ie and "isento" in ie.strip().lower() else (1 if ie else 0),

        "shortName": suffix_remover(format_name(resp["fantasia"])) if resp["fantasia"] else suffix_remover(format_name(resp["nome"])),
        "name": format_name(resp["nome"]),
        "mainNIF": resp["cnpj"].strip(),
        "stateRegister": ie,
        "zipCode": format_zipcode(resp["cep"]),
        "streetType": format_street(resp["logradouro"])[0],
        "streetName": format_street(resp["logradouro"])[1],
        "number": resp["numero"].upper().strip(),
        "districtType": format_district(resp["bairro"])[0],
        "district": format_district(resp["bairro"])[1],
        "stateCode": resp["uf"].upper().strip(),
        "cityInternalId": "",  # Formatar
        "phoneNumber": format_phone(resp["telefone"]),
        "email": resp["email"].lower().strip()
    }
    
    return response
