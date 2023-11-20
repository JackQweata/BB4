from typing import Any
from utils.models import session, Problems, Complexity


def selection_problems_bot(topic_user: Any, rating: int) -> list:
    """ Перебирает и ищет для пользователя задания по его фильтрам. Вернет 10 классов Problems"""

    problems = []
    list_bd = session.query(Problems).join(Complexity).filter(Complexity.values == rating).all()

    for item in list_bd:
        if sorted(topic_user, key=lambda x: x.id) == sorted(item.topics, key=lambda x: x.id):
            problems.append(item)

    return problems[:10]
