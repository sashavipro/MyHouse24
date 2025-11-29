FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       netcat-openbsd \
       gcc \
       libpq-dev \
       libcairo2 \
       libpango-1.0-0 \
       libpangocairo-1.0-0 \
       libgdk-pixbuf-2.0-0 \
       libffi-dev \
       shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app/

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
