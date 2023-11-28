from typing import Any
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.modules.callback_factory import PaginateCallbackFactory, FilterSelectCallbackFactory, \
    SelectionUserCallbackFactory

user_data = {}
server_data = {}


def get_keyboard_next_filters(user_bd) -> Any:
    """ Инлайн кнопка приветственного письма с переходом в главное меню """

    if user_bd.telegram not in user_data:
        user_data[user_bd.telegram] = {
            'user': user_bd,
            'rating': {'page': 0, 'selects': None},
            'topic': {'page': 0, 'selects': []},
            'selection': {}
        }

    filter_bt = InlineKeyboardBuilder()
    filter_bt.button(
        text='Фильтры',
        callback_data='filters'
    )

    return filter_bt.as_markup()


def get_keyboard_main_filter() -> Any:
    """
        Инлайн кнопки главного меню:
        1_bt - Выбор сложность
        2_bt - Выбор темы
        3_bt - Подборка, на основе выбранных фильтров
    """

    filter_settings_bt = InlineKeyboardBuilder()

    filter_settings_bt.button(
        text='Сложность 🧠',
        callback_data='rating'
    )
    filter_settings_bt.button(
        text='Тема 📝',
        callback_data='topic'
    )
    filter_settings_bt.button(
        text='Подобрать 🔍',
        callback_data='search'
    )

    filter_settings_bt.adjust(2, 1)
    return filter_settings_bt.as_markup()


def get_keyboard_settings_filter(user_id: int, filters_bd: list, type_filter: str) -> Any:
    """ Инлайн кнопки с выбором фильтров """

    slice_list = [filters_bd[i:i + 10] for i in range(0, len(filters_bd), 10)]
    builder = InlineKeyboardBuilder()

    if type_filter not in server_data:
        server_data[type_filter] = {
            'count_page': len(slice_list),
            'select_page': {}
        }

    count_page = server_data[type_filter]['count_page']
    user_page = user_data[user_id][type_filter]['page']
    user_select = user_data[user_id][type_filter]['selects']

    for item in slice_list[user_page]:

        message_text = ' ✅' if item == user_select else ''
        if type_filter == 'topic':
            message_text = ' ✅' if item in user_select else ''

        server_data[type_filter]['select_page'][item.id] = item

        builder.button(
            text=str(item.values)[:20] + message_text,
            callback_data=FilterSelectCallbackFactory(values=item.id, belongs=type_filter)
        )

    callback_next_event = 'next_event'
    callback_prev_event = 'prev_even'

    if count_page > user_page + 1:
        callback_next_event = PaginateCallbackFactory(action='next', page=1, belongs=type_filter)

    if user_page > 0:
        callback_prev_event = PaginateCallbackFactory(action='prev', page=-1, belongs=type_filter)

    builder.button(
        text="⬅️ Назад",
        callback_data=callback_prev_event
    )

    builder.button(
        text="Следующая ➡️",
        callback_data=callback_next_event
    )

    builder.button(
        text='В меню 🏠',
        callback_data='main'
    )

    builder.adjust(2, 2)
    return builder.as_markup()


def get_keyboard_search_problems(user_id: int, problems: list) -> Any:
    """ Инлайн кнопки с подобранными задачами по фильтрам """

    search_problems_bt = InlineKeyboardBuilder()
    topic_select = user_data[user_id]['topic']['selects']
    rating_select = user_data[user_id]['rating']['selects']

    if topic_select or rating_select:

        for index, item in enumerate(problems):
            user_data[user_id]['selection'][index] = item

            search_problems_bt.button(
                text=item.title,
                callback_data=SelectionUserCallbackFactory(index=index)
            )

    search_problems_bt.button(
        text='В меню 🏠',
        callback_data='main'
    )

    search_problems_bt.adjust(1)
    return search_problems_bt.as_markup()
