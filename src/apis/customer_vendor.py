import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


def create_new_customer_vendor(
        companyId: str,
        code: str,
        shortName: str,
        name: str,
        type: int,
        mainNIF: str,
        stateRegister: str,
        zipCode: str,
        streetType: str,
		streetName: str,
		number: str,
		districtType: str,
		district: str,
		countryInternalId: str,
		stateCode: str,
		cityInternalId: str,
		phoneNumber: str,
		email: str,
        contributor: int
):
    try:
        load_dotenv(override=True)

        api_url = os.getenv("API_URL")
        api_user = os.getenv("API_USER")
        api_user_pwd = os.getenv("API_USER_PWD")

        session = requests.Session()
        session.auth = HTTPBasicAuth(api_user, api_user_pwd)
        session.headers.update({"Accept": "application/json"})

        json = {
            "companyId": companyId,
            "code": code,
            "companyInternalId": f"{companyId}|{code}",
            "shortName": shortName,
            "name": name,
            "type": type,
            "entityType": "J",
            "mainNIF": mainNIF,
            "stateRegister": stateRegister,
            "registerSituation": 1,
            "address": {
                "zipCode": zipCode,
                "streetType": streetType,
                "streetName": streetName,
                "number": number,
                "districtType": districtType,
                "district": district,
                "country": {
                    "countryInternalId": countryInternalId
                },
                "state": {
                    "stateCode": stateCode
                },
                "city": {
                    "cityInternalId": cityInternalId
                },
                "communicationInformation": {
                    "phoneNumber": phoneNumber,
                    "email": email
                }
            },
            "contributor": contributor,
            "fuelOperationType": 3,
            "complementaryFields": {
                "codcoligada": int(companyId),
                "codcfo": code
            }
        }
        
        resp = session.post(api_url, json=json, timeout=30)
        resp.raise_for_status()
    
    except Exception as e:
        print(f"exception: {e}")
