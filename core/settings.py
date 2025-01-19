import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expire_minutes: int = os.getenv('DATABASE_URL')
    database_url: str = os.getenv('DATABASE_URL')
    model_name: str = os.getenv('MODEL_NAME')
    auth_token: str = os.getenv('HUGGING_FACE_KEY')