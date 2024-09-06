import multiprocessing

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GunicornSettings(BaseModel):
    WORKER_PER_CORE: int = Field(1)
    MAX_WORKERS: int = Field(3)

    @field_validator("MAX_WORKERS")
    def assemble_max_workers(cls, v: int) -> int:
        if v < 3:
            return 3
        else:
            return v

    MAX_REQUESTS: int = Field(3000)
    MAX_REQUESTS_JITTER: int = Field(1500)
    GRACEFUL_TIMEOUT: int = Field(60)
    TIMEOUT: int = Field(120)
    KEEPALIVE: int = Field(75)
    HOST: str = Field("0.0.0.0")
    PORT: int = Field(8000)
    LOG_LEVEL: str = Field("info")
    ERROR_LOG: str = Field("-")
    ACCESS_LOG: str = Field("-")


class Settings(BaseSettings):
    GUNICORN: GunicornSettings = Field(GunicornSettings())  # type: ignore

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        case_sensitive=True,
    )


settings = Settings()  # type: ignore

cores = multiprocessing.cpu_count()
default_web_concurrency = settings.GUNICORN.WORKER_PER_CORE * cores

bind = f"{settings.GUNICORN.HOST}:{settings.GUNICORN.PORT}"
workers = int(max(default_web_concurrency, settings.GUNICORN.MAX_WORKERS))
worker_tmp_dir = "/dev/shm"
max_requests = settings.GUNICORN.MAX_REQUESTS
max_requests_jitter = settings.GUNICORN.MAX_REQUESTS_JITTER
graceful_timeout = settings.GUNICORN.GRACEFUL_TIMEOUT
timeout = settings.GUNICORN.TIMEOUT
keepalive = settings.GUNICORN.KEEPALIVE
loglevel = settings.GUNICORN.LOG_LEVEL
accesslog = settings.GUNICORN.ACCESS_LOG
errorlog = settings.GUNICORN.ERROR_LOG
