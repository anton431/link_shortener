"""controller."""
from sqlalchemy.orm import Session

from src.app.config.database import link_storage


def add_current_link(long_link: str, session: Session):
    """Add_short_link.

    Args:
        long_link (str): long_link
        session (Session): The database session

     Returns:
        bool: successful add
    """
    return link_storage.add(long_link, session)


def get_current_link(link_id: str, session: Session):
    """Get long link.

    Args:
        link_id(str): link_id
        session (Session): The database session

    Returns:
        str: long_link
    """
    return link_storage.get_link(link_id, session)


def delete_current_link(long_link: str, session: Session):
    """Delete_short_link.

    Args:
        long_link (str): long_link
        session (Session): The database session
    """
    link_storage.delete(long_link, session)
