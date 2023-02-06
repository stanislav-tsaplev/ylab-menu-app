FROM python:3.10-slim
WORKDIR /src
ENV PYTHONPATH=/app

RUN mkdir /xls
VOLUME [ "/xls" ]

COPY requirements.txt alembic.ini ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY migrations/ ./migrations
COPY app/ ./app
