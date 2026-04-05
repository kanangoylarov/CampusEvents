FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libc6-dev zlib1g-dev libjpeg62-turbo-dev libfreetype-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--preload", "run:app"]
