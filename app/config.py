from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    super_admin_password: str
    super_admin_email: EmailStr

    class Config:
        env_file = ".env"

settings = Settings()