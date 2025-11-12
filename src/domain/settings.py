from pydantic_settings import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    # SERVICE
    SERVICE_NAME: str = 'ticketing'
    RELOAD: bool = False
    PORT: int = 8000
    HOST: str = '0.0.0.0'
    NAMESPACE: str
    API_VERSION: str = 'v1'
    RESOURCE: str
    IMAGE_VERSION: str = 'v1'

    # DATABASE
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_DATABASE: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()
