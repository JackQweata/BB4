import asyncio
import logging

from src.bot_menager import start_telegram_bot
from src.parser_menager import data_extraction
from utils.models import session, Problems


def first_filling() -> None:
    """ Заполняет пустую бд (первый запуск) """

    logging.basicConfig(level=logging.INFO)

    problems = session.query(Problems).count()

    if not problems:
        data_extraction()

    asyncio.run(start_telegram_bot())


if __name__ == '__main__':
    first_filling()
