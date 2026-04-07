import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Sử dụng GEMINI_API_KEY được AI Studio cung cấp sẵn
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini-2.5-flash" # Model nhanh và hiệu quả cho Agent
    TEMPERATURE = 0
    
settings = Settings()
