"""models."""
from sqlalchemy import Column, Integer, String

from src.app.config.config import Base


class Link(Base):
    """Table Link."""

    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)
    link_id = Column(String(10), unique=True)
    short_link = Column(String(50))  # noqa: WPS432
    long_link = Column(String(1000))
