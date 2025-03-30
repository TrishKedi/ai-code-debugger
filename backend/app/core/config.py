import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    OPENAI_KEY: str = os.getenv("OPEN_AI_KEY")

settings = Settings()
