# syntax=docker/dockerfile:1
FROM python:3.10 as base

WORKDIR /opt/assets
WORKDIR /opt/src

COPY requirments.txt .

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install -r requirments.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

ENV PYTHONPATH=/opt
COPY src /opt/src

CMD ["python", "main.py"]
