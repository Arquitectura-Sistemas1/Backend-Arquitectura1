"""Environment-based configuration for the Resend integration."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ResendConfig:
    api_key: str
    from_email: str


def get_resend_config() -> ResendConfig:
    return ResendConfig(
        api_key=os.getenv("RESEND_API_KEY", ""),
        from_email=os.getenv("RESEND_FROM_EMAIL", ""),
    )
