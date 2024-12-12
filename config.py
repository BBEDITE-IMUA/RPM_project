from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str
    RABBITMQ_HOST: str
    class Config:
        env_file = '.env'
        extra = 'ignore'

settings = Settings()