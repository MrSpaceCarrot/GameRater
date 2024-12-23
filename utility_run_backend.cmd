@echo off
call backend\venv\Scripts\activate
cd backend
python manage.py runserver 0.0.0.0:15001