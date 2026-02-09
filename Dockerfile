# ===== STAGE 1: builder =====
FROM python:3.14-slim-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# ===== STAGE 2: runtime =====
FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Только runtime-зависимости: libpq — для подключения к PostgreSQL, curl - для отладки health-check
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Копируем всё из builder (включая .venv и код)
COPY --from=builder /app /app/

RUN groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["granian", "--interface", "asgi", "src.main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8000", "--access-log"]
