from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config.database import get_db

from src.app.views.link import app
from src.app.config.config import Settings
from src.app.models.models import Base

engine = create_engine(Settings.SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


app.dependency_overrides[get_db] = get_test_db

session = TestingSessionLocal()

client = TestClient(app)
