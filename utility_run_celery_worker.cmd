@echo off
call backend\venv\Scripts\activate
cd backend
celery -A gamerater worker --loglevel=info --pool=solo