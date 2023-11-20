import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import config
from src.modules.callback_factory import PaginateCallbackFactory, FilterSelectCallbackFactory, \
    SelectionUserCallbackFactory
from src.modules.context_menu_mixin import menu_selectors_filter_mixin, menu_main_mixin
from src.modules.keyboards import get_keyboard_next_filters, get_keyboard_settings_filter, \
    user_data, server_data, get_keyboard_search_problems
from src.modules.selection_problems import selection_problems_bot
from utils.models import session, User, Complexity, TopicProblems


async def start_telegram_bot() -> None:
    """ Запуск бота telegram """

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    users_all = session.query(User).all()

    for item in users_all:
        await bot.edit_message_text(
            chat_id=item.telegram,
            message_id=item.last_message,
            text="Ма обновили бота\nСпасибо, что вы с нами😉",
            reply_markup=get_keyboard_next_filters(item)
        )

    @dp.message(Command('start'))
    async def start(message: types.Message):

        user_id = message.from_user.id
        user_bd = session.query(User).filter_by(telegram=user_id).first()

        if user_bd and user_bd.last_message > 0:
            try:
                await bot.delete_message(chat_id=user_id, message_id=user_bd.last_message)
            except Exception:
                logging.info(f"Сообщения пользователя {user_id} не найдено")
        else:
            user_bd = User(name=message.from_user.first_name, telegram=user_id)

        session.add(user_bd)

        message_user = await message.answer(
            text=f"Привет, {user_bd.name}!\nДавай подберем для тебя задачки 😉\n\nㅤ",
            reply_markup=get_keyboard_next_filters(user_bd)
        )

        user_bd.last_message = message_user.message_id

        session.commit()

    @dp.callback_query(F.data == "main")
    async def send_random_value(callback: types.CallbackQuery):
        await menu_main_mixin(callback)

    @dp.callback_query(F.data == "filters")
    async def send_random_value(callback: types.CallbackQuery):
        await menu_main_mixin(callback)

    @dp.callback_query(F.data == "rating")
    async def callback_rating(callback: types.CallbackQuery):

        ratings_bd = session.query(Complexity).all()

        await callback.message.edit_text(
            text="Сложность",
            reply_markup=get_keyboard_settings_filter(callback.from_user.id, ratings_bd, 'rating')
        )

    @dp.callback_query(F.data == "topic")
    async def callback_topic(callback: types.CallbackQuery):

        topic_bd = session.query(TopicProblems).all()

        await callback.message.edit_text(
            text="Темы",
            reply_markup=get_keyboard_settings_filter(callback.from_user.id, topic_bd, 'topic')
        )

    @dp.callback_query(F.data == "search")
    async def callback_topic(callback: types.CallbackQuery):

        problems = []
        user_id = callback.from_user.id
        topic_select = user_data[user_id]['topic']['selects']
        rating_select = user_data[user_id]['rating']['selects']

        if not topic_select:
            message_text = 'Ну установлена тема задачи\n\nㅤ'
        elif not rating_select:
            message_text = 'Ну установлена сложность задачи\n\nㅤ'
        else:
            message_text = 'Вот что мы нашли\nㅤ'
            problems = selection_problems_bot(topic_select, rating_select.values)

            if not problems:
                message_text = 'Мы ничего не смогли подобрать 😔\nㅤ'

                user_data[user_id]['topic']['selects'] = []
                user_data[user_id]['rating']['selects'] = None

        await callback.message.edit_text(
            text=message_text,
            reply_markup=get_keyboard_search_problems(user_id, problems)
        )

    @dp.callback_query(PaginateCallbackFactory.filter())
    async def callbacks_paginate_filter_fab(
            callback: types.CallbackQuery,
            callback_data: PaginateCallbackFactory
    ):

        user_id = callback.from_user.id
        types_filter = callback_data.belongs

        user_data[user_id][types_filter]['page'] += callback_data.page

        await menu_selectors_filter_mixin(callback, callback_data)

    @dp.callback_query(FilterSelectCallbackFactory.filter())
    async def callbacks_filter_select(
            callback: types.CallbackQuery,
            callback_data: FilterSelectCallbackFactory
    ):

        user_id = callback.from_user.id
        types_filter = callback_data.belongs
        server_select = server_data[types_filter]['select_page'][callback_data.values]
        user_select = user_data[user_id][types_filter]['selects']

        if types_filter == 'topic':
            if server_select not in user_select:
                user_select.append(server_select)
            else:
                user_select.remove(server_select)
        else:
            user_data[user_id][types_filter]['selects'] = server_select

        await menu_selectors_filter_mixin(callback, callback_data)

    @dp.callback_query(SelectionUserCallbackFactory.filter())
    async def callbacks_selection_user(
            callback: types.CallbackQuery,
            callback_data: SelectionUserCallbackFactory
    ):
        user_id = callback.from_user.id
        problem = user_data[user_id]['selection'][callback_data.index]
        topics = [topic.values for topic in problem.topics]
        problems = [value for key, value in user_data[user_id]['selection'].items()]

        message_text = (
            f'ㅤ\n\nНазвание: 📣 {problem.title} {problem.contestId} 📣\n\n'
            f'Сложность: {problem.complexity.values} 🧠\n\n'
            f'Темы: {" ,".join(topics)} 📝\n\n'
            f'Количество решений: {problem.count_solutions} 👨‍👨‍👦‍👦\n\nㅤ'
        )

        await callback.message.edit_text(
            text=message_text,
            reply_markup=get_keyboard_search_problems(user_id, problems)
        )

    await dp.start_polling(bot)
