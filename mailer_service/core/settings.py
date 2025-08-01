from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    kafka_bootstrap_servers: str
    kafka_topic: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=".env") 