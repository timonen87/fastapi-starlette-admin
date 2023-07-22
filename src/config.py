import os

from dotenv import load_dotenv
from typing import Optional

from pydantic import BaseSettings

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET_AUTH = os.environ.get("SECRET_AUTH")

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")


class Config(BaseSettings):
    sqla_engine: str = "sqlite:///demo.db?check_same_thread=false"
    mongo_uri: str = "mongodb://127.0.0.1:27017/demo"
    mongo_host: str = "mongodb://127.0.0.1:27017/"
    mongo_db: str = "demo"
    upload_dir: str = "upload/"
    secret: str = "123456789"
    gtag: Optional[str] = None


config = Config()