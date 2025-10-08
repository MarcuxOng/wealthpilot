from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    gemini_api_key: str 
    gemini_model: str

    app_host: str
    app_port: int 

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_database: str

    origin: str

settings = Settings()
