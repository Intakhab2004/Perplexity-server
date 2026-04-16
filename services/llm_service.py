from groq import Groq
from helpers.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """
    You are a helpful AI assistant which solves user's query and give the response in formatted way.
"""


class LLMService:
    def ai_response(self, prompt: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        try:
            formatted_message = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]

            res = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=formatted_message,
                temperature=0.7
            )

            return res.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"LLM error: { str(e)}")

    
llm_service = LLMService()
