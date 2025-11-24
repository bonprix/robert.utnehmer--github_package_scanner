FROM python:3.11-slim

COPY . /app

WORKDIR /app

RUN pip install -e .

RUN useradd --create-home --shell /bin/bash appuser
USER appuser

ENTRYPOINT ["/usr/local/bin/github-ioc-scan"]
