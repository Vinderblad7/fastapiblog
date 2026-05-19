from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_NAME: str = "blog.db"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")