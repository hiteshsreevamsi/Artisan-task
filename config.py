from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    openai_api_key: str
    sqlalchemy_database_url: str
    hugging_face_api_key: str

    class Config:
        env_file = ".env"


# Create a settings instance
settings = Settings()
