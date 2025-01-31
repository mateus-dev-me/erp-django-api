FROM python:3.11-alpine

LABEL maintainer="mateus-dev-me.com.br"
LABEL description="ERP API container with Python and Poetry"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

COPY scripts /scripts
COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

EXPOSE 8000

CMD ["commands.sh"]
