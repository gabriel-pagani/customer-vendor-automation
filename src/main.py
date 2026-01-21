from apis.customer_vendor import create_new_customer_vendor
from apis.receitaws import cnpj_lookup

resp = cnpj_lookup("5", "F99999", 2, "18.236.120/0001-58", "123456789")

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
