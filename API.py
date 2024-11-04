from flask import Flask, request, make_response, jsonify
import json
from os import path

from Library import LibraryManager
from Bunny import BunnyAPI

HOME_DIR = path.dirname(path.realpath(__file__))
UPLOAD_DIR = path.join(HOME_DIR, "uploads")

api = Flask(__name__)
api_Bunny = BunnyAPI()
api_Library = LibraryManager()

def wkw(**kwargs):
    return kwargs

def BuildHTTPResponse(
        headers: dict = None,
        status_code = 200, **kwargs
    ):

    type = kwargs.get("type")
    message = kwargs.get("message")
    message_name = kwargs.get("message_name")

    route = kwargs.get("route")
    method = kwargs.get("method")

    object = kwargs.get("object")


    resp = make_response()
    resp.status_code = status_code

    if headers is not None:
        resp.headers = headers
    else:
        resp.headers.set("Content-Type", "application/json")
        resp.headers.set("Server", "video")
        resp.headers.set("Date", datetime.datetime.now())
        
    data = {
        "type": type, # Response type

        "message": message, # Response type message
        "message_name": message_name, # Response data object name (internal)

        "route": route, # Request route
        "method": method, # Request method
        
        "object": object # Response data object
    }

    resp.set_data(
        json.dumps(data, indent=4)
    )

    return resp

@api.route("/library/register", methods=["POST"])
def register_library():
    if request.json is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No JSON Payload provided!",
            message_name = "no_payload_provided"
        ))
    
    accessor = request.json.get("Accessor")
    if accessor is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No accessor provided!",
            message_name = "no_accessor_provided"
        ))
    
    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    if user_data is None:
        api_Library.create_new_user(google_id=accessor)
        user_data = (None, {}, None)

    user_metadata = user_data[1]
    if user_metadata.get("library") is not None:
        return jsonify(wkw(
            type = "WARN",
            message = f"User is already registered!",
            message_name = "user_already_registered"
        ))

    library_creation = api_Bunny.library_Create(name=accessor)
    if library_creation['message_name'] != "library_creation_success":
        return jsonify(wkw(
            type = "FAIL",
            message = f"Error creating library",
            message_name = "library_registration_fail"
        ))
    library = library_creation['object']

    api_Library.associate_library_with_googleid(
        library_id = library['Id'],
        google_id = accessor
    )

    return jsonify(wkw(
        type = "WARN",
        message = f"User registered successfully!",
        message_name = "library_registration_success"
    ))