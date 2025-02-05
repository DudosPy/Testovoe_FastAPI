import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    mysql_host: str = os.getenv("MYSQL_HOST", "mysql")
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "root")
    mysql_db: str = os.getenv("MYSQL_DB", "delivery_service")
    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    mongo_host: str = os.getenv("MONGO_HOST", "mongo")
    mongo_port: int = int(os.getenv("MONGO_PORT", 27017))
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "rabbitmq")

settings = Settings()