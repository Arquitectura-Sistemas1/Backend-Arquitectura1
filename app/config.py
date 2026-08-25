from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Declaras tus variables de entorno y sus tipos
    DATABASE_URL2: str

    # Pydantic busca automáticamente el archivo .env en la raíz del proyecto
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instancia global accesible en toda la app
settings = Settings()