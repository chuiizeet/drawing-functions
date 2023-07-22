import json
from random import randint
from datetime import datetime
from appwrite.client import Client
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.id import ID


def main(req, res):
    api_key = req.variables.get("APPWRITE_API_KEY", "No key no mames")
    endpoint = req.variables.get("APPWRITE_ENDPOINT", "No key no mames")
    project_id = req.variables.get("APPWRITE_FUNCTION_PROJECT_ID", "No key no mames")
    database_id = req.variables.get("DATABASE_ID", "No key no mames")

    # Create client
    client = Client()

    (
        client.set_endpoint(endpoint)  # Your API Endpoint
        .set_project(project_id)  # Your project ID
        .set_key(api_key)  # Your secret API key
        .set_self_signed(True)
    )

    # Database
    databases = Databases(client)

    trigger = req.variables["APPWRITE_FUNCTION_TRIGGER"]
    event_data = req.variables.get("APPWRITE_FUNCTION_EVENT_DATA", None)
    users_collection_id = req.variables["USERS_COLLECTION_ID"]

    if not event_data:
        return res.json(
            {
                "message": f"Bad trigger: {trigger}",
            },
            400,
        )

    """
	! We use session object bc: https://github.com/appwrite/appwrite/issues/5198
	Session Object: https://appwrite.io/docs/models/session
	userId: To create user on table
	"""
    document_trigger = json.loads(event_data)
    user_id = document_trigger["userId"]

    if not user_id:
        return res.json(
            {
                "message": f"userId not in event data",
            },
            501,
        )

    try:
        # Check if user already exists...
        queries = [Query.equal("userId", user_id)]
        total = databases.list_documents(
            database_id=database_id,
            collection_id=users_collection_id,
            queries=queries,
        )["total"]
        if total > 0:
            return res.json(
                {
                    "message": f"{user_id} already exists.",
                    "success": True,
                },
                200,
            )

        # Create user with random username...
        curr_dt = datetime.now()
        timestamp = int(round(curr_dt.timestamp()))
        random_numer = randint(0, 5)
        random_user_name = f"guest-{timestamp}-{random_numer}"
        create_user = databases.create_document(
            collection_id=users_collection_id,
            database_id=database_id,
            document_id=ID.unique(),
            data={
                "userId": user_id,
                "username": random_user_name,
            },
        )
        return res.json(
            {
                "message": f"{create_user}",
                "success": True,
            }
        )
        return res.json(
            {
                "message": f"User created successfully: {response}",
                "success": True,
            },
            201,
        )
    except Exception as e:
        return res.json(
            {
                "message": f"Unknow error: {e}",
                "success": False,
            },
            500,
        )
