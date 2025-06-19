import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
from dotenv import load_dotenv

os.environ.clear()
load_dotenv()

class Settings(BaseSettings):
    
    VERIFY_TOKEN: str = Field(..., env="VERIFY_TOKEN")


settings = Settings()
