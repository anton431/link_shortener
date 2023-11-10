"""database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.config.config import Settings
from src.app.data_sources.storages.link import LinkStorage

engine = create_engine(Settings.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

link_storage = LinkStorage()


def get_db():
    """Get db.

    Yields:
        Session: SessionLocal
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
