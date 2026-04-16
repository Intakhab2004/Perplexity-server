from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timezone


class PlanSchema(BaseModel):
    query: str
    plan: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PlanHistory(BaseModel):
    user_id: str
    plan_history: List[PlanSchema]