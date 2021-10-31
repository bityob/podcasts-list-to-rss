FROM python:3.10.0

ARG TELEGRAM_APP_ID
ARG TELEGRAM_APP_HASH
ARG TELEGRAM_PUBLIC_CHANNEL_NAME

ENV TELEGRAM_APP_ID=$TELEGRAM_APP_ID
ENV TELEGRAM_APP_HASH=$TELEGRAM_APP_HASH
ENV TELEGRAM_PUBLIC_CHANNEL_NAME=$TELEGRAM_PUBLIC_CHANNEL_NAME

WORKDIR /app
RUN mkdir assets

COPY requirments.txt .

RUN pip install -r requirments.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY app /app
COPY user.session /app

ENV PYTHONPATH=/

CMD ["python", "main.py"] 