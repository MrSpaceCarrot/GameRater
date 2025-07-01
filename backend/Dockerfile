FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache \
    bash \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    && python -m pip install --no-cache-dir --upgrade pip setuptools

RUN addgroup -S gameratergroup && adduser -S gamerateruser -G gameratergroup

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs && \
    chown -R gamerateruser:gameratergroup /app/logs

RUN chown -R gamerateruser:gameratergroup /app

USER gamerateruser

EXPOSE 15001

ENV TERM=xterm
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["bash", "-c", "python manage.py collectstatic --noinput && celery -A gamerater worker --concurrency=2 --loglevel=info & celery -A gamerater beat --loglevel=info & gunicorn --bind 0.0.0.0:15001 --workers 1 gamerater.wsgi:application"]