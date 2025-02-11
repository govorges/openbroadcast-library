from flask import Flask, request, jsonify
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

    library_creation_response = api_Bunny.library_Create(name=accessor)
    try:
        library = library_creation_response.json()
    except json.JSONDecodeError:
        return jsonify(wkw(
            type = "FAIL",
            message = f"Error creating library",
            message_name = "library_registration_fail"
        ))

    api_Library.associate_library_with_googleid(
        library_id = library['Id'],
        google_id = accessor
    )

    return jsonify(wkw(
        type = "INFO",
        message = f"User registered successfully!",
        message_name = "library_registration_success"
    ))

@api.route("/library/metadata", methods=['GET'])
def library_metadata():
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
    user_metadata = user_data[1]

    return jsonify(user_metadata)


@api.route("/library/collections", methods=['GET'])
def library_collections():
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
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    collections = api_Bunny.library_Collections(user_library)
    collections = collections['items']

    return jsonify(collections)

@api.route('/library/collections/add', methods=['POST'])
def library_collections_add():
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
    
    collection_name = request.json.get("collection_name")
    if collection_name is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No collection name provided!",
            message_name = "no_collection_name_provided"
        ))
    
    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    collection = api_Bunny.library_Collection_Create(
        user_library, collection_name=collection_name
    )
    return jsonify(collection)

@api.route("/library/collections/delete", methods=['POST'])
def library_collections_delete():
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
    
    collection_guid = request.json.get("guid")
    if collection_guid is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No collection guid provided!",
            message_name = "no_collection_guid_provided"
        ))

    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    collection = api_Bunny.library_Collection_Delete(
        user_library, collection_guid = collection_guid
    )
    return jsonify(collection)

@api.route("/library/collections/update", methods=['POST'])
def library_collections_update():
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
    
    collection_guid = request.json.get("guid")
    if collection_guid is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No collection guid provided!",
            message_name = "no_collection_guid_provided"
        ))
    
    collection_name = request.json.get("name")
    if collection_name is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No collection name provided!",
            message_name = "no_collection_name_provided"
        ))

    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    collection = api_Bunny.library_Collection_Update(
        user_library, collection_guid = collection_guid, collection_name = collection_name
    )
    return jsonify(collection)

@api.route("/library/videos", methods=['GET'])
def library_videos():
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
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    videos = api_Bunny.library_Videos(user_library)
    videos = videos['items']

    return jsonify(videos)

@api.route("/library/videos/<videoId>", methods=['GET'])
def library_videos_retrieve(videoId):
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
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    video = api_Bunny.library_Video_Retrieve(user_library, videoId)

    return jsonify(video)


@api.route("/library/upload/create", methods=['POST'])
def createUploadSignature():
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
    
    videoId = request.json.get("videoId")
    if videoId is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No videoId provided!",
            message_name = "no_videoid_provided"
        ))

    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    signature_data = api_Bunny.library_Upload_CreateSignature(user_library, videoId)
    if signature_data is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"Upload signature creation failed!",
            message_name = "signature_creation_failed"
        ))
    signature_data['libraryId'] = user_library
    signature_data['videoId'] = videoId
    
    return jsonify(signature_data)
    
@api.route("/library/videos/create", methods=['POST'])
def createVideoObject():
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
    
    video_data = request.json.get("video_data")
    if video_data is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No data provided!",
            message_name = "no_data_provided"
        ))
    if video_data.get("title") is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No title provided!",
            message_name = "no_title_provided"
        ))
    
    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    user_metadata = user_data[1]
    user_library = user_metadata['library']

    video_data = api_Bunny.library_Video_Create(
        libraryId = user_library, 
        video_data = video_data
    )
    return video_data
    
@api.route("/library/update", methods=['POST'])
def updateLibrary():
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
    
    payload = request.json.get("payload")
    if payload is None:
        return jsonify(wkw(
            type = "FAIL",
            message = f"No data provided!",
            message_name = "no_data_provided"
        ))
    
    user_data = api_Library.retrieve_user_by_google_id(google_id=accessor)
    user_metadata = user_data[1]
    user_library = user_metadata['library']
    
    update_response = api_Bunny.library_Update(
        libraryId = user_library,
        payload = payload
    )
    return jsonify(update_response)

@api.route("/library/details", methods=['GET'])
def libraryDetails():
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
    user_metadata = user_data[1]
    user_library = user_metadata['library']
    
    retrieval_response = api_Bunny.library_Retrieve(
        libraryId = user_library
    )

    return jsonify(retrieval_response)

