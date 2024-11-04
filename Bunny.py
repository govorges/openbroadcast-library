import requests
from os import environ

class BunnyAPI:
    def __init__(self):
        self.API_Endpoint_URL = environ["BUNNY_ENDPOINT_ADDRESS"]
    def library_Create(self, name: str):
        payload = {
            "Name": name
        }
        request = requests.get(f"http://{self.API_Endpoint_URL}/library/create", json=payload)
        return request.json()

    def library_Retrieve(self, id: str):
        request = requests.get(f"http://{self.API_Endpoint_URL}/library/{id}")
        return request.json()
    
    def library_Update(self, id: str, payload: dict):
        request = requests.post(f"http://{self.API_Endpoint_URL}/library/{id}", data=payload)
        return request.json()
    
