from time import sleep
from apis.customer_vendor import create_new_customer_vendor
from apis.receitaws import cnpj_lookup
from database.connection import execute_query
from constants.customers_vendors import customers_vendors


for cnpj, infos in customers_vendors.items():
    try:
        data = execute_query("""
            SELECT
                'F' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'F%' AND CODCOLIGADA in (1,5,6) ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_FOR,
                'C' + RIGHT('00000' + CAST((CAST(SUBSTRING((SELECT TOP 1 CODCFO FROM FCFO WHERE CODCFO LIKE 'C%' AND CODCOLIGADA in (1,5,6) ORDER BY DATACRIACAO DESC, CODCFO DESC), 2, 5) AS INT) + 1) AS VARCHAR), 5) AS COD_CLI
        """)
        codcfo = data[0][1] if infos[0].lower() == "c" else data[0][0]
        
        resp = cnpj_lookup(codcoligada="5", codcfo=codcfo, cnpj=cnpj, ie=infos[1])

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

        sleep(20)

    except Exception as e:
        print(f"exception: {e}")
