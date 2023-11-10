import pytest

from src.app.config.database import link_storage
from src.tests.conftest import session


def test_LinkStorage_generate_unique_link_id():
    link_id = link_storage.generate_unique_link_id(session)
    assert len(link_id) == 6


@pytest.mark.parametrize("long_link, session",
[
    pytest.param("https://shift.cft.ru/python", session, id="successful test_LinkStorage_generate_unique_link_id"),
    pytest.param("https://shift.cft.ru/python", session, id="successful test_LinkStorage_generate_unique_link_id"),
    pytest.param("https://www.youtube.com/", session, id="successful test_LinkStorage_generate_unique_link_id"),
]
)
def test_LinkStorage_add(long_link, session):
    link = link_storage.add(long_link=long_link, session=session)
    assert link.long_link == long_link


def test_LinkStorage_get_link():
    with pytest.raises(ValueError):
        link = link_storage.get_link(link_id="link_id", session=session)
