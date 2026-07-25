from pydantic_settings import BaseSettings 
from dotenv import load_dotenv
import os


load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "CV Analytics Service"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    class Config:
        env_file = ".env"
        
        
settings = Settings()