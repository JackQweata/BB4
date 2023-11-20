# Дипломная работа по парсингу Сodeforces (BB4)
    1) заполнить .env
    3) выполнить команды:
        1. pip install -r requirements.txt
        2. celery -A scheduled_task beat --loglevel=info
        3. celery -A tasks worker --loglevel=info
    4) Запустить проект