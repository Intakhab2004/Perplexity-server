from database.config import plan_collection
from database.models.query_plan import PlanSchema
from typing import List


class DBService:
    def save_query_plan(self, user_id: str, query: str, plan: List[str]):
        try:
            plan_collection.update_one(
                {"user_id": user_id},
                {
                    "$push": {
                        "plan_history": PlanSchema(
                                query=query, 
                                plan=plan
                            ).model_dump()
                    }
                },
                upsert=True
            )

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        

db_service = DBService()