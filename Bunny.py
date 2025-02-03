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

    def library_Retrieve(self, libraryId: str):
        request = requests.post(f"http://{self.API_Endpoint_Address}/videolibrary/{libraryId}", json={})

        return request.json()
    
    def library_Collections(self, id: str):
        request = requests.get(f"http://{self.API_Endpoint_Address}/library/{id}/collections", json={})

        return request.json()
    
    def library_Videos(self, id: str):
        request = requests.get(f"http://{self.API_Endpoint_Address}/library/{id}/videos?itemsPerPage=1000", json={})

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
            json = video_data
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
    
    def library_Collection_Delete(self, libraryId, collection_guid: str):
        request = requests.delete(
            f"http://{self.API_Endpoint_Address}/library/{libraryId}/collections/{collection_guid}",
            json={}
        )
        return request.json()
    
    def library_Collection_Update(self, libraryId, collection_guid: str, collection_name: str):
        request = requests.post(
            f"http://{self.API_Endpoint_Address}/library/{libraryId}/collections/{collection_guid}",
            json = {
                "name": collection_name
            }
        )
        return request.json()
    
    def library_Video_Retrieve(self, libraryId, videoId):
        request = requests.get(
            f"http://{self.API_Endpoint_Address}/library/{libraryId}/videos/{videoId}",
            json = {}
        )
        return request.json()
    
    def library_Update(self, libraryId, payload):
        request = requests.post(
            f"http://{self.API_Endpoint_Address}/videolibrary/{libraryId}",
            json = payload
        )
        return request.json()