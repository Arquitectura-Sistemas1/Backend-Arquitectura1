from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL2: str
    RESEND_KEY: str
    CLOUDNANE : str
    CLOUDKEY: str
    CLOUDSECRET: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()