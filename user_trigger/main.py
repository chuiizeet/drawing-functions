import json
from random import randint
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query
from datetime import datetime
from random import randint


def main(req, res):
    API_KEY = req.variables.get("API_KEY")
    APPWRITE_ENDPOINT = req.variables.get("APPWRITE_ENDPOINT")
    PROJECT_ID = req.variables.get("APPWRITE_FUNCTION_PROJECT_ID", "No key no mames")
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

    # Database
    databases = Databases(client)

    TRIGGER_DATA = req.variables.get("APPWRITE_FUNCTION_EVENT_DATA", "ERROR")

    try:
        trigger_json = json.loads(TRIGGER_DATA)
        user_id = trigger_json["$id"]

        # Verify if user exist
        queries = [Query.equal(attribute="userId", value=user_id)]
        response = databases.list_documents(
            collection_id=USERS_COLLECTION_ID,
            database_id=DATABASE_ID,
            queries=queries,
        )

        # User already exists...
        if response["total"] != 0:
            return res.json(
                {"message": f"User {user_id} already exists", "success": True}
            )

        # Create user
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))
        random_numer = randint(0, 5)
        random_user_name = f"guest-{timestamp}-{random_numer}"
        create_user = databases.create_document(
            collection_id=USERS_COLLECTION_ID,
            database_id=DATABASE_ID,
            document_id=ID.unique(),
            data={
                "userId": user_id,
                "username": random_user_name,
            },
        )
        return res.json({"message": f"{create_user}", "success": True})
    except Exception as e:
        return res.json({"message": f"{e}", "success": False})
