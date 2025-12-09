# syntax=docker/dockerfile:1
FROM python:3.10 AS base

WORKDIR /opt/assets
WORKDIR /opt/src

COPY --from=ghcr.io/astral-sh/uv:0.9.16 /uv /uvx /bin/

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/tmp/venv
ENV UV_COMPILE_BYTECODE=1
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_NO_SYNC=1
ENV UV_FROZEN=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=src/pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=src/uv.lock,target=uv.lock \
    uv sync --no-install-project
    
COPY src .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

ENV PYTHONPATH=/opt

CMD ["uv", "run", "main.py"]
