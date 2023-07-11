import json


def main(req, res):
    payload = (
        req.payload or "No payload provided. Add custom data when executing function."
    )

    API_KEY = req.variables.get(
        "API_KEY",
    )
    APPWRITE_ENDPOINT = req.variables.get(
        "APPWRITE_ENDPOINT",
    )
    DRAWS_COLLECTION_ID = req.variables.get(
        "DRAWS_COLLECTION_ID",
    )
    DATABASE_ID = req.variables.get(
        "DATABASE_ID",
    )

    try:
        payload = json.loads(payload)
        user_id = payload["userId"]
        return res.json({"message": user_id, "success": True})

    except Exception as e:
        return res.json({"message": f"{e}", "success": False})
