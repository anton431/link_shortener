FROM python:3.10-slim-bullseye 

ENV PYSETUP_PATH="/opt/pysetup"

WORKDIR $PYSETUP_PATH

COPY ./init-container/requirements.txt .

RUN pip install -r requirements.txt

COPY ./src/alembic.ini ./src/alembic.ini
COPY ./src/app/migrations ./src/app/migrations
COPY ./src/app/config ./src/app/config
COPY ./src/app/models ./src/app/models

#CMD ["alembic", "-c", "src/alembic.ini", "upgrade", "head"]