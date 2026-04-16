from fastapi import APIRouter
from pydantic import BaseModel
from database.config import queries_collection
from database.models.user_query import Queries
from database.schemas.query_schema import query_history
from database.models.user_query import Query
from services.llm_service import llm_service
from agents.planner_agent import generate_plan

router = APIRouter()

@router.get("/test")
def test_route():
    return {
        "status": "success",
        "message": "API Router is connected to main app and is working fine."
    }


class QueryRequest(BaseModel):
    userId: str
    query: str

@router.post("/user-query")
def post_query(req: QueryRequest):
    try:
        user = queries_collection.find_one({"userId": req.userId})
        ai_reply = llm_service.ai_response(req.query)
        generate_plan(query=req.query, user_id=req.userId)
        
        if user:
            queries_collection.update_one(
                {"userId": req.userId},
                {
                    "$push": {
                        "history": {
                            "$each": [
                                Query(content=req.query).model_dump(),
                                Query(content=ai_reply).model_dump()
                            ]
                        }
                    }
                }
            )

        else:
            new_user = Queries(
                userId=req.userId,
                history=[
                    Query(content=req.query),
                    Query(content=ai_reply)
                ]
            )

            queries_collection.insert_one(new_user.model_dump())

        return {
            "success": True,
            "message": "User query saved",
            "reply": ai_reply
        }
    except Exception as e:
        return {
            "success": False,
            "detail": f"Internal server error: {str(e)}"
        }


@router.get("/get-history/{userId}")
def get_chat_history(userId: str):
    try:
        user = queries_collection.find_one({"userId": userId})
        if not user:
            return {
                "success": False,
                "history": []
            }
        else:
            return {
                "success": True,
                "history": query_history(user)
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }