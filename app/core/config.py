from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Cloudinary
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    # Google OAuth
    google_client_id: str
    google_client_secret: str

    # Email
    mail_username: str
    mail_password: str
    # mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str = "ChattyBee"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False

    #Resend Email
    resend_api_key: str
    mail_from: str
    # Frontend
    frontend_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()