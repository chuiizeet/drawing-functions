import json
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.services.databases import Databases
from appwrite.id import ID


def main(req, res):
    """
    payload: => {postId: str, userId: str, title: str, imageId: str}
    draw:=> {postId: str, imageId: str, userId: str, title: str, userDocumentId: str}
    """
    payload = (
        req.payload or "No payload provided. Add custom data when executing function."
    )

    API_KEY = req.variables.get("API_KEY")
    APPWRITE_ENDPOINT = req.variables.get("APPWRITE_ENDPOINT")
    PROJECT_ID = req.variables.get("APPWRITE_FUNCTION_PROJECT_ID")
    DRAWS_COLLECTION_ID = req.variables.get("DRAWS_COLLECTION_ID")
    USERS_COLLECTION_ID = req.variables.get("USERS_COLLECTION_ID")
    DATABASE_ID = req.variables.get("DATABASE_ID")

    # Create client
    client = Client()

    (
        client.set_endpoint(APPWRITE_ENDPOINT)  # Your API Endpoint
        .set_project(PROJECT_ID)  # Your project ID
        .set_key(API_KEY)  # Your secret API key
        .set_self_signed(True)
    )

    storage = Storage(client)
    databases = Databases(client)

    try:
        payload: dict = json.loads(payload)
        post_id = payload.get("postId", None)
        user_id = payload.get("userId", None)
        image_id = payload.get("imageId", None)
        user_document_id = payload.get("userDocumentId", None)
        title = payload.get("title", "")

        if post_id == None or user_id == None:
            raise Exception("postId or userId missing")

        if image_id == None:
            raise Exception("imageId missing")

        if user_document_id == None:
            raise Exception("userDocumentId missing")

        response = databases.create_document(
            database_id=DATABASE_ID,
            collection_id=DRAWS_COLLECTION_ID,
            document_id=ID.unique(),
            data={
                "postId": post_id,
                "imageId": image_id,
                "userId": user_id,
                "title": title,
            },
        )

        _id = response["$id"]

        # Update Score and draws by userId
        myUser = databases.get_document(
            database_id=DATABASE_ID,
            collection_id=USERS_COLLECTION_ID,
            document_id=user_document_id,
        )

        score = myUser["score"]
        draws = myUser["draws"]

        databases.update_document(
            database_id=DATABASE_ID,
            collection_id=USERS_COLLECTION_ID,
            document_id=user_document_id,
            data={
                "score": score + 1,
                "draws": draws + 1,
            },
        )

        return res.json(
            {
                "message": f"Draw uploaded correctly",
                "success": True,
                "drawId": _id,
            }
        )

    except Exception as e:
        return res.json({"message": f"{e}", "success": False})
