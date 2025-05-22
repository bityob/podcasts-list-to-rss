# syntax=docker/dockerfile:1
FROM python:3.10 as base

WORKDIR /opt/assets
WORKDIR /opt/src

COPY requirments.txt .

#RUN --mount=type=cache,target=/var/cache/apt,sharing=locked  \
#    --mount=type=cache,target=/var/lib/apt,sharing=locked \
#    apt update && \
#    apt install libnss3 \
#                libdbus-1-3 \
#                libatk1.0-0 \
#                libatk-bridge2.0-0 \
#                libcups2 \
#                libdrm2 \
#                libxcomposite1 \
#                libxdamage1 \
#                libxfixes3 \
#                libxrandr2 \
#                libgbm1 \
#                libxkbcommon0 \
#                libasound2 -y

RUN --mount=type=cache,mode=0755,target=/root/.cache/pip \
    pip install -r requirments.txt

ENV PYTHONPATH=/opt

COPY src /opt/src

#RUN cd /opt/src && pytest ./utils.py -vvv -s

CMD ["python", "main.py"]
