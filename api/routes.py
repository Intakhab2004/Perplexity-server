from fastapi import APIRouter
from pydantic import BaseModel
from database.config import queries_collection
from database.schemas.query_schema import query_history
from agents.planner_agent import generate_plan
from typing import List
from agents.search_agent import search
from services.chunking_service import generate_chunks
from services.vector_store import store_embeddings
from agents.answer_agent import generate_answer

router = APIRouter()

@router.get("/test")
def test_route():
    return {
        "status": "success",
        "message": "API Router is connected to main app and is working fine."
    }


class QueryRequest(BaseModel):
    user_id: str
    query: str

@router.post("/ask")
def ask_question(req: QueryRequest):
    try:
        plan = generate_plan(query=req.query, user_id=req.user_id)
        if not plan:
            raise ValueError("Error occured while generating plan")
        
        search_agent_content = search(plan)
        if not search_agent_content:
            raise ValueError("Error occured during web search")
        
        chunks = generate_chunks(search_agent_content)
        if not chunks:
            raise ValueError("Something went wrong while generating the chunks")
        
        info = store_embeddings(chunks)
        if not info == "completed":
            raise ValueError("Something went wrong while storing embeddings")
        
        result = generate_answer(req.query)
        if not result:
            raise ValueError("Something went wrong while answer llm call")
        
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        print("Something went wrong: ", str(e))
        return {
            "success": False,
            "message": f"Internal server error: {str(e)}"
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