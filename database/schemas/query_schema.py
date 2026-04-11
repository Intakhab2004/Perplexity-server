def individual_query_schema(query):
    return {
        "id": str(query["id"]),
        "userId": query["userId"],
        "history": query["history"]
    }

def query_history(query):
    return query["history"]