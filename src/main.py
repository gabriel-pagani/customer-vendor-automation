from apis.customer_vendor import create_new_customer_vendor
from apis.receitaws import cnpj_lookup

resp = cnpj_lookup(coligada="5", code="F99999", cnpj="07.150.434/0001-17", ie="256016631")

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
