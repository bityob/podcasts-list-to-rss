FROM python:3.10.0

RUN pip install -r requirments.txt

WORKDIR /app

COPY src /app

CMD ["bash", "main.py"]