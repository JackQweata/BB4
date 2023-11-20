from typing import Optional

from aiogram.filters.callback_data import CallbackData


class PaginateCallbackFactory(CallbackData, prefix="fabnum"):
    """ Фабрика пагинации списков """

    belongs: str
    action: str
    page: Optional[int] = 0


class FilterSelectCallbackFactory(CallbackData, prefix="select"):
    """ Фабрика выбора пользователя в фильтрах """

    belongs: str
    values: int


class SelectionUserCallbackFactory(CallbackData, prefix="select"):
    """ Фабрика выбора пользователя в подборе задачи """

    index: int
