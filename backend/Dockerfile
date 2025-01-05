FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache \
    bash gcc libpq-dev musl-dev && \
    apk add --no-cache --virtual .build-deps gcc libpq-dev musl-dev && \
    apk del .build-deps

RUN addgroup -S gameratergroup && adduser -S gamerateruser -G gameratergroup

RUN python -m pip install --no-cache-dir --upgrade pip setuptools

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R gamerateruser:gameratergroup /app

USER gamerateruser

EXPOSE 15001

ENV TERM=xterm
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["bash", "-c", "celery -A gamerater worker --loglevel=info & celery -A gamerater beat --loglevel=info & gunicorn --bind 0.0.0.0:15001 --workers 1 gamerater.wsgi:application"]
