import os
import requests
from dotenv import load_dotenv
from utils.formatter import (
    format_name, 
    suffix_remover, 
    format_zipcode, 
    format_street, 
    format_number,
    format_district, 
    format_municipality, 
    format_phone
)


def cnpj_lookup(codcfo: str, cnpj: str, ie: str = ""):
    load_dotenv(override=True)

    api_id = os.getenv("QIVE_API_ID")
    api_key = os.getenv("QIVE_API_KEY")

    if not api_id or not api_key:
        raise RuntimeError("Missing environmental variables")
    
    formatted_cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    
    url = f"https://api.arquivei.com.br/v1/cnpj/{formatted_cnpj}"
    
    headers = {
        "X-API-ID": api_id,
        "X-API-KEY": api_key,
        "X-Use-ApiGateway": "always"
    }

    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    resp = r.json()

    data = resp.get("data", {})

    if (isinstance(resp, dict) and resp.get("status") == "ERROR") or data.get("status") == "ERROR":
        raise RuntimeError(resp.get("message"))

    response = {
        "status": data.get("situacao", ""),
        "code": codcfo,
        "shortName": suffix_remover(format_name(data.get("fantasia", ""))) if data.get("fantasia") else suffix_remover(format_name(data.get("nome", ""))),
        "name": format_name(data.get("nome", "")),
        "type": 1 if codcfo.upper().startswith('C') else (2 if codcfo.upper().startswith('F') else 3),  # 1 = Cliente | 2 = Fornecedor | 3 = Ambos
        "mainNIF": data.get("cnpj", cnpj).strip(),
        "stateRegister": ie if ie and "isento" not in ie.lower() else "",
        "zipCode": format_zipcode(data.get("cep", "")),
        "streetType": format_street(data.get("logradouro", ""))[0],
        "streetName": format_street(data.get("logradouro", ""))[1],
        "number": format_number(data.get("numero", "")),
        "complement": data.get("complemento", "").title().strip(),
        "districtType": format_district(data.get("bairro", ""))[0],
        "district": format_district(data.get("bairro", ""))[1],
        "stateCode": data.get("uf", "").upper().strip(),
        "cityInternalId": format_municipality(data.get("municipio", ""), data.get("uf", "")),
        "phoneNumber": format_phone(data.get("telefone", "")),
        "email": data.get("email", "").lower().strip(),
        "contributor": 2 if ie and "isento" in ie.lower() else (1 if ie else 0)  # 0 = Não contribuinte | 1 = Contribuinte | 2 = Isento
    }

    return response
