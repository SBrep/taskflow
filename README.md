# TaskFlow

Простой HTTP-сервис управления задачами (in-memory).

## Запуск

venv/Scripts/activate
pip install -r requirements.txt
uvicorn cmd.server.main:app --reload