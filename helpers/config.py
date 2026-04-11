from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.DB_URI = os.getenv("DB_URI")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not self.DB_URI:
            raise ValueError("DB_URI is missing in .env")
        
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in .env")
        
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing in .env")
        
settings = Settings()
