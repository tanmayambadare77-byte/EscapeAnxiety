from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "replace_this_with_a_secure_random_string"
    DATABASE_URL: str = "sqlite:///./escape_anxiety.db"
    JWT_EXPIRATION_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    MODEL_PATH: str = "app/ml/mood_model.pkl"

    class Config:
        env_file = ".env"


settings = Settings()
