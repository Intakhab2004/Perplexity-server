from services.llm_service import llm_service
from services.db_service import db_service
import re


PLANNER_PROMPT = """
    You are a research planning assistant.

    Given a user query, break it into 4-6 clear, specific sub-questions 
    that can be used to perform deep research.

    Rules:
    - Keep questions concise
    - Avoid repetition
    - Cover different aspects
    - Return ONLY a numbered list.
    - Do not include any explanation, intro, or extra text.
"""

def generate_plan(query: str, user_id: str):
    llm_response = llm_service.ai_response(query, PLANNER_PROMPT)
    if not llm_response:
        raise ValueError("Invalid response from LLM")
    
    # Format response
    formatted_output = [re.sub(r'^\s*(\d+[\.\-\)]|\•|\-)\s*', '', line)
                        for line in llm_response.splitlines() if line.strip()]
    
    if not formatted_output:
        raise ValueError("No valid plan generated")

    db_service.save_query_plan(user_id, query, formatted_output)

    return formatted_output

