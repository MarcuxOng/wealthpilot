from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Gemini API Configuration
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash-exp"
    
    # App Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8080


settings = Settings()
