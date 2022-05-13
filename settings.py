from pydantic import BaseSettings
from pydantic.main import Path


class Settings(BaseSettings):

    # Files settings
    STATIC_DIR_PREFIX: Path = 'static'
    STATIC_DIR_PATH: str = f'/{STATIC_DIR_PREFIX}/'

    UPLOAD_DIR: Path = STATIC_DIR_PREFIX + '/uploads/'
    RESULT_DIR: Path = STATIC_DIR_PREFIX + '/results/'

    # Model settings
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.75


settings = Settings()
