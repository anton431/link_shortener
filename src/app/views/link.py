"""API modul."""
from contextlib import asynccontextmanager

import aiojobs
import validators
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from jaeger_client import Config
from prometheus_client import make_asgi_app
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_200_OK

from src.app.config.config import Settings
from src.app.config.database import get_db
from src.app.link.controller import (add_current_link, delete_current_link,
                                     get_current_link)
from src.app.middlewares import metrics_count_middleware, tracing_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan.

    Args:
        app (FastAPI): FastAPI

    Yields:
        dict: jaeger_tracer
    """
    conf = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': Settings.JAGER_HOST,
                'reporting_port': Settings.JAGER_PORT,
            },
            'logging': True,
        },
        service_name='adontsov-servic-src-link',
        validate=True,
    )
    tracer = conf.initialize_tracer()
    scheduler = aiojobs.Scheduler()
    yield {
        'jaeger_tracer': tracer,
    }

    await scheduler.close()

app = FastAPI(lifespan=lifespan)


@app.post('/api/short')
async def short(url: str, session: Session = Depends(get_db)):
    """Link shortener.

    Args:
        url (str): long url
        session (Session): The database session

    Raises:
        HTTPException: Incorrect url

    Returns:
        json: short url
    """
    if not validators.url(url):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect url',
        )

    link = add_current_link(long_link=url, session=session)
    return JSONResponse(content={'short_link': link.short_link})


@app.get('/short/{link_id}')
async def redirect(link_id: str, session: Session = Depends(get_db)):
    """Redirects to the long link associated with the given link_id.

    Args:
        link_id (str): The link_id to retrieve the long link
        session (Session): The database session

    Returns:
        RedirectResponse: A redirect response to the long link
    """
    long_link = get_current_link(link_id=link_id, session=session).long_link
    return RedirectResponse(
        url=long_link, status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )


@app.delete('/api/short/delete')
async def short_delete(url: str, session: Session = Depends(get_db)):
    """Link delete.

    Args:
        url (str): long url
        session (Session): The database session

    Raises:
        HTTPException: Incorrect url

    Returns:
        json: url deleted
    """
    if not validators.url(url):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect url',
        )

    delete_current_link(long_link=url, session=session)
    return JSONResponse(content={'deleted': url})


@app.get('/healthz/ready')
async def ready(session: Session = Depends(get_db)):
    """Ready.

    Args:
        session (Session): The database session

    Raises:
        HTTPException: Failed to connect to the database

    Returns:
        int: status
    """
    try:
        session.execute(text('SELECT 1'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to connect to the database',
        )
    return HTTP_200_OK


@app.get('/healthz/up')
async def up():
    """Up.

    Returns:
        int: status
    """
    return HTTP_200_OK

metrics_app = make_asgi_app()  # Инициализация ASGI-сервера для передачи метрик
app.mount('/metrics', metrics_app)
app.add_middleware(BaseHTTPMiddleware, dispatch=metrics_count_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=tracing_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
