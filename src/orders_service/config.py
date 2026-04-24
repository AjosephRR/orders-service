import bcrypt
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    environment: str = "development"
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1_440)
    database_url: str = "sqlite:///./orders.db"
    db_echo: bool = False
    auth_username: str = Field(min_length=1)
    auth_password_hash: SecretStr

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long.")
        return value

    @field_validator("auth_password_hash")
    @classmethod
    def validate_auth_password_hash(cls, value: SecretStr) -> SecretStr:
        password_hash = value.get_secret_value().encode("utf-8")

        try:
            bcrypt.checkpw(b"settings-validation", password_hash)
        except ValueError as exc:
            raise ValueError("AUTH_PASSWORD_HASH must be a valid bcrypt hash.") from exc

        return value


def load_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = load_settings()
