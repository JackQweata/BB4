from config import app
from src.parser_menager import data_extraction


@app.task
def run_parser():
    """ Задача по парсингу, запуск каждый час """

    data_extraction()


if __name__ == '__main__':
    app.start()
