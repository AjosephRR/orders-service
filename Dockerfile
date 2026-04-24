# ---------- BUILDER ----------
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# ---------- RUNTIME ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN useradd --system --create-home --home-dir /home/appuser --shell /usr/sbin/nologin appuser

COPY --from=builder /usr/local /usr/local
COPY --chown=appuser:appuser src/ ./src
COPY --chown=appuser:appuser alembic.ini .
COPY --chown=appuser:appuser alembic/ ./alembic
COPY --chown=appuser:appuser entrypoint.sh .

RUN sed -i 's/\r$//' entrypoint.sh \
    && chmod 500 entrypoint.sh \
    && chown appuser:appuser /app

USER appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["./entrypoint.sh"]
