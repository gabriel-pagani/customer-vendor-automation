from apis.customer_vendor import create_new_customer_vendor
from apis.receitaws import cnpj_lookup

try:
    resp = cnpj_lookup(codcoligada="5", codcfo="F99999", cnpj="07.150.434/0001-17", ie="256016631")

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

except Exception as e:
    print(f"exception: {e}")
