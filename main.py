import asyncio
from src.bot_menager import start_telegram_bot
from src.parser_menager import data_extraction
from utils.models import session, Problems


def first_filling():
    """ Заполняет пустую бд (первый запуск) """

    problems = session.query(Problems).count()

    if not problems:
        data_extraction()


if __name__ == '__main__':
    first_filling()
    asyncio.run(start_telegram_bot())
