from pydantic_settings import BaseSettings
from pydantic import ValidationError, PostgresDsn, AnyHttpUrl, ConfigDict
from typing import Literal

#Get config From the .env file
class Settings(BaseSettings):
    DB_URL : PostgresDsn
    QUEUE_URL : str
    LLM_ENDPOINT : AnyHttpUrl
    ENV : Literal["dev", "prod"] = "dev"
    
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",  # Add any other previous config options here
    )
try:
    Config = Settings()
except ValidationError as e:
    msgerror = e.errors()[0]['msg']
    print(f"Error: {msgerror}")
    