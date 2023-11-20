from src.modules.keyboards import get_keyboard_settings_filter, get_keyboard_main_filter, user_data
from utils.models import session, TopicProblems, Complexity


async def menu_selectors_filter_mixin(callback, callback_data):

    user_id = callback.from_user.id
    types_filter = callback_data.belongs

    if types_filter == 'topic':
        list_bd = session.query(TopicProblems).all()
        message_text = 'Темы 👾'
    else:
        list_bd = session.query(Complexity).all()
        message_text = 'Сложность🔥'

    await callback.message.edit_text(
        text=f'{message_text}\nСтраница: {user_data[user_id][types_filter]["page"] + 1}',
        reply_markup=get_keyboard_settings_filter(user_id, list_bd, types_filter)
    )


async def menu_main_mixin(callback):
    """ Миксин с главным меню """

    user_id = callback.from_user.id
    select_rating = user_data[user_id]['rating']['selects']
    select_topic = user_data[user_id]['topic']['selects']
    message_text = 'Установленные фильтры ⚙️\n\n'

    if select_rating:
        message_text += f'Сложность: {select_rating.values}\n\n'
    if select_topic:
        message_text += f'Тема: {" ,".join([t.values for t in select_topic])}\n\n'

    elif not select_rating and not select_topic:
        message_text = 'Фильтры не установлены 😔\n\n'

    await callback.message.edit_text(
        text=message_text,
        reply_markup=get_keyboard_main_filter()
    )