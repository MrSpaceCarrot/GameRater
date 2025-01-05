@echo off
call backend\venv\Scripts\activate
cd backend
celery -A gamerater beat --loglevel=info