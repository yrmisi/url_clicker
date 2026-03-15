FROM python:3.14.2-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY src/ ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

COPY docker_build/src/entrypoint.sh ./scripts/entrypoint.sh

RUN chmod +x ./scripts/entrypoint.sh

FROM python:3.14.2-slim-trixie

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/ /app/

RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]

CMD ["granian", "main:app", \
     "--interface", "asgi", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--runtime-threads", "1", \
     "--loop", "uvloop", \
     "--backlog", "1024", \
     "--backpressure", "128", \
     "--workers-max-rss", "512", \
     "--rss-samples", "3", \
     "--rss-sample-interval", "10s", \
     "--workers-lifetime", "1h", \
     "--log-level", "warning", \
     "--access-log"]
