"""storage.link."""
import uuid

from sqlalchemy.orm import Session

from src.app.config.config import Settings
from src.app.models.models import Link


class LinkStorage():
    """Link storage."""

    def generate_unique_link_id(self, session: Session):
        """Generate unique link id.

        Args:
            session (Session): The database session

        Returns:
            str: unique link_id
        """
        unique_link_id = str(uuid.uuid4())[:6]

        link_exist = session.query(Link).filter(
            Link.link_id == unique_link_id,
        ).first()

        if link_exist:
            return self.generate_unique_link_id()

        return unique_link_id

    def add(self, long_link: str, session: Session) -> Link:
        """Add new link.

        Args:
            long_link (str): long_link
            session (Session): The database session

        Returns:
            Link: Link
        """
        link_exist = session.query(Link).filter(
            Link.long_link == long_link,
        ).first()

        if link_exist:
            return link_exist

        unique_link_id = self.generate_unique_link_id(session)
        short_link = f'http://{Settings.SRC_HOST}:{Settings.SRC_PORT}/short/{unique_link_id}'  # noqa: E501

        new_link = Link(
            long_link=long_link,
            short_link=short_link,
            link_id=unique_link_id,
        )
        session.add(new_link)
        session.commit()
        session.refresh(new_link)

        return new_link

    def delete(self, long_link: str, session: Session):
        """Delete new link.

        Args:
            long_link (str): long_link
            session (Session): The database session
        """
        session.query(Link).filter(
            Link.long_link == long_link,
        ).delete()
        session.commit()

    def get_link(self, link_id: str, session: Session) -> Link:
        """Get link.

        Args:
            link_id (str): link_id
            session (Session): The database session

        Raises:
            ValueError: Link not exist

        Returns:
            Link: Link
        """
        link_exist = session.query(Link).filter(
            Link.link_id == link_id,
        ).first()

        if not link_exist:
            raise ValueError('Link not exist')

        return link_exist
