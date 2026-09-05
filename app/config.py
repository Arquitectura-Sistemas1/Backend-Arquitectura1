"""Configuración central del backend basada en variables de entorno."""

from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL2: str
    RESEND_KEY: str = ""
    RESEND_API_KEY: str = ""
    RESEND_FROM_EMAIL: str = ""
    CLOUDNANE: str
    CLOUDKEY: str
    CLOUDSECRET: str
    KEY_JWT: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


@dataclass(frozen=True)
class ResendConfig:
    api_key: str
    from_email: str


def get_resend_config() -> ResendConfig:
    return ResendConfig(
        api_key=settings.RESEND_API_KEY or settings.RESEND_KEY,
        from_email=settings.RESEND_FROM_EMAIL,
    )
