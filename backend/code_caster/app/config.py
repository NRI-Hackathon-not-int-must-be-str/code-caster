import secrets

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str = Field(secrets.token_urlsafe(32))
    MEDIA_PATH: str = Field("media")


settings = Settings()  # type: ignore
