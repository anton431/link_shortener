"""service modul."""
import uvicorn

from src.app.config.config import Settings
from src.app.views.link import app

if __name__ == '__main__':
    uvicorn.run(app, host=Settings.SRC_HOST, port=int(Settings.SRC_PORT))
