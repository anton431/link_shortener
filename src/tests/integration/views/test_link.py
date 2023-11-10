from urllib.parse import urlparse

import pytest

from src.tests.conftest import client

@pytest.mark.parametrize("client, expected",
[
    pytest.param(client, 200, id="successful test_ready")
]
)
def test_ready(client, expected):
    response = client.get("/healthz/ready")
    assert response.status_code == expected


@pytest.mark.parametrize("client, url, expected",
[
    pytest.param(client,'https://stepik.org/users/546578473/profile', 200, id="successful test_short"),
    pytest.param(client,'url', 404, id="url test_short"),
    pytest.param(client,'', 404, id="empty test_short"),
    pytest.param(client,'https://stepik', 404, id="part link test_short"),
    pytest.param(client,
                 'https://www.google.ru/search?q=some+queries&newwindow=1&sca_esv=576056213&source=hp&ei=0ZE3ZeqrFJKQwPAP68KFuAM&iflsig=AO6bgOgAAAAAZTef4UPHpW8o2E4zeva1CWYQBrvsz6tr&oq=some+query&gs_lp=Egdnd3Mtd2l6Igpzb21lIHF1ZXJ5KgIIAjIFEAAYgAQyBhAAGBYYHjILEAAYFhgeGPEEGAoyCBAAGBYYHhgPMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeSN6NAVCwLliEdXADeACQAQCYAfUBoAGDC6oBBTYuNS4xuAEByAEA-AEBqAIKwgIQEC4YAxiPARjlAhjqAhiMA8ICEBAAGAMYjwEY5QIY6gIYjAPCAgsQABiKBRixAxiDAcICCxAAGIAEGLEDGIMBwgILEC4YigUYsQMYgwHCAhEQLhiABBixAxiDARjHARjRA8ICDhAuGIAEGLEDGMcBGNEDwgIIEAAYgAQYsQPCAgQQABgDwgIFEC4YgATCAgsQLhiABBjHARjRA8ICCBAuGIAEGLEDwgILEC4YgAQYsQMYgwHCAgsQLhiDARixAxiABA&sclient=gws-wiz', 
                 200,
                 id="long long link test_short"),
]
)
def test_short(client, url, expected):
    data_params = {'url': url}
    response = client.post("/api/short", params=data_params)
    status_code = response.status_code
    assert status_code == expected
    if status_code == 200:
        url = response.json().get('short_link')
        short_link = urlparse(url).path
        response_redirect = client.get(url=short_link,  allow_redirects=False)
        assert response_redirect.status_code == 301


@pytest.mark.parametrize("client, url, expected",
[
    pytest.param(client,'https://stepik.org/users/546578473/profile', 200, id="successful test_short"),
    pytest.param(client,'https://stepik.org/users/546578473/profile', 200, id="successful test_short"),
    pytest.param(client,'url', 404, id="url test_short"),
    pytest.param(client,'', 404, id="empty test_short"),
    pytest.param(client,'https://stepik', 404, id="part link test_short")
]
)
def test_short_delete(client, url, expected):
    data_params = {'url': url}
    response = client.delete("/api/short/delete", params=data_params)
    status_code = response.status_code
    assert status_code == expected
        
