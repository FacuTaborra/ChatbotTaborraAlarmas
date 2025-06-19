import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    VERIFY_TOKEN: str = Field(..., env="VERIFY_TOKEN")
    API_KEY: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    MODEL: str = Field(default_factory=lambda: os.getenv("MODEL"))

    WHATSAPP_PHONE_ID: str = Field(default_factory=lambda: os.getenv("WHATSAPP_PHONE_ID"))
    WHATSAPP_ACCESS_TOKEN: str = Field(default_factory=lambda: os.getenv("WHATSAPP_ACCESS_TOKEN"))

    DB_HOST: str = Field(default_factory=lambda: os.getenv("DB_HOST"))
    DB_PORT: Optional[int] = Field(default_factory=lambda: int(os.getenv("DB_PORT", 3306)))
    DB_NAME: str = Field(default_factory=lambda: os.getenv("DB_NAME"))
    DB_USER_READER: str = Field(default_factory=lambda: os.getenv("DB_USER_READER"))
    DB_PASS_READER: str = Field(default_factory=lambda: os.getenv("DB_PASS_READER"))
    DB_USER_WRITER: str = Field(default_factory=lambda: os.getenv("DB_USER_WRITER"))
    DB_PASS_WRITER: str = Field(default_factory=lambda: os.getenv("DB_PASS_WRITER"))
    
settings = Settings()
