import os
from datetime import timedelta
from celery import Celery
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)


BD_CONNECT = (f'postgresql://{os.getenv("BD_USER")}:{os.getenv("BD_PASS")}@'
              f'{os.getenv("BD_HOST")}:{os.getenv("BD_PORT")}/{os.getenv("BD_NAME")}')

SITE_DOMAIN = "https://codeforces.com/"

BOT_TOKEN = os.getenv('BOT_API_KEY')

app = Celery('tasks', broker=os.getenv('BROKER_CELERY'))
