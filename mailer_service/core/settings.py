from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    kafka_bootstrap_servers: str
    kafka_topic: str
    
    redis_url: str

    smtp_host: str 
    smtp_port: int 
    smtp_user: str 
    smtp_password: str
    smtp_from: str 
    smtp_tls: bool 


    model_config = SettingsConfigDict(env_file=".env") 