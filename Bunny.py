import requests
from os import environ

class BunnyAPI:
    def __init__(self):
        self.API_Endpoint_Address = environ["BUNNY_ENDPOINT_ADDRESS"]
    def library_Create(self, name: str):
        payload = {
            "Name": name
        }
        request = requests.post(f"http://{self.API_Endpoint_Address}/videolibrary", json=payload)
        
        return request

    def library_Retrieve(self, id: str):
        request = requests.get(f"http://{self.API_Endpoint_Address}/videolibrary/{id}")
        
        return request.json()
    
    def library_CollectionsRetrieve(self, id: str):
        request = requests.get(f"http://{self.API_Endpoint_Address}/library/{id}/collections", json={})

        return request.json()
    
    def library_VideosRetrieve(self, id: str):
        request = requests.get(f"http://{self.API_Endpoint_Address}/library/{id}/videos", json={})

        return request.json()
    
    def library_Update(self, id: str, payload: dict):
        request = requests.post(f"http://{self.API_Endpoint_Address}/library/{id}", json=payload)
        return request.json()
    
    def library_Upload_CreateSignature(self, libraryId, videoId):
        request = requests.get(f"http://{self.API_Endpoint_Address}/library/{libraryId}/videos/{videoId}/create_upload_signature")
        return request.json()

    def library_Video_Create(self, libraryId, video_data: dict):
        request = requests.post(
            f"http://{self.API_Endpoint_Address}/library/{libraryId}/videos",
            data = video_data
        )
        return request.json()

    def library_Collection_Create(self, libraryId, collection_name: str):
        request = requests.post(
            f"http://{self.API_Endpoint_Address}/library/{libraryId}/collections",
            json = {
                "name": collection_name
            }
        )
        
        return request.json()