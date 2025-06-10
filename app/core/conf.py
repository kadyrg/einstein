from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: str
    DB_HOST: str
    DB_ECHO: bool = False


    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_VALIDITY: int = 365 # days


    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_USER: str
    EMAIL_PASS: str


    OTP_VALIDITY: int = 5 # minutes

    R2_ACCOUNT_TOKEN_VALUE: str
    R2_ACCOUNT_ACCESS_KEY: str
    R2_ACCOUNT_SECRET_KEY: str

    R2_USER_TOKEN_VALUE: str
    R2_USER_ACCESS_KEY_ID: str
    R2_USER_SECRET_KEY_ID: str

    ENDPOINT_URL: str

    BUCKET_NAME: str

    MEDIA_ROOT: Path = BASE_DIR / "app/media"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    class Config:
        env_file = BASE_DIR / '.env'
        env_file_encoding='utf-8'


settings = Settings()
