"""config modul."""
import os

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

load_dotenv()

Base: DeclarativeMeta = declarative_base()


class Settings:
    """Secrets."""

    SRC_HOST = os.getenv('SRC_HOST')
    SRC_PORT = os.getenv('SRC_PORT')
    JAGER_HOST = os.getenv('JAGER_HOST')
    JAGER_PORT = os.getenv('JAGER_PORT')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername='postgresql',
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )

    SQLALCHEMY_DATABASE_URL_TEST = URL.create(
        drivername='postgresql',
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=f'{POSTGRES_DB}_test',
    )
