import json
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.services.databases import Databases
from appwrite.id import ID


def main(req, res):
    """
    payload: => {drawId: str}    
    """
    payload = (
        req.payload or "No payload provided. Add custom data when executing function."
    )

    API_KEY = req.variables.get("API_KEY")
    APPWRITE_ENDPOINT = req.variables.get("APPWRITE_ENDPOINT")
    PROJECT_ID = req.variables.get("APPWRITE_FUNCTION_PROJECT_ID")
    DRAWS_COLLECTION_ID = req.variables.get("DRAWS_COLLECTION_ID")    
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
        draw_id = payload.get("drawId", None)
        
        if draw_id == None:
            raise Exception("drawId is missing")
        
        # Update Score and draws by userId
        current_draw = databases.get_document(
            database_id=DATABASE_ID,
            collection_id=DRAWS_COLLECTION_ID,
            document_id=draw_id,
        )

        up_votes: int  = current_draw["upVotes"]        
        new_up_votes: int  = up_votes + 1
        

        databases.update_document(
            database_id=DATABASE_ID,
            collection_id=DRAWS_COLLECTION_ID,
            document_id=draw_id,
            data={
                "upVotes": new_up_votes,                
            },
        )

        return res.json(
            {
                "message": f"Success",
                "success": True,
                "upVotes": new_up_votes,
            }
        )

    except Exception as e:
        return res.json({"message": f"{e}", "success": False})
