from utils.codeforces import CodeforcesApi
from utils.models import session, Problems, TopicProblems, Complexity


def data_extraction() -> None:

    api = CodeforcesApi()
    problems = api.task_parsing()

    for item in problems:

        problem_id = f"{item['contestId']}{item['index']}"
        is_bd = session.query(Problems).filter(Problems.contestId == problem_id).first()

        if is_bd:
            continue

        new_problem = Problems(
            contestId=problem_id,
            title=item['name'],
            count_solutions=item['solvedCount']
        )
        session.add(new_problem)

        rating = session.query(Complexity).filter(Complexity.values == item.get('rating', 0)).first()

        if not rating:
            rating = Complexity(values=item.get('rating', 0))
            session.add(rating)

        new_problem.complexity = rating

        tags_problem = list(set(item['tags']))

        for tag in tags_problem:
            topic = session.query(TopicProblems).filter(TopicProblems.values == tag).first()

            if not topic:
                topic = TopicProblems(values=tag)
                session.add(topic)

            new_problem.topics.append(topic)

    session.commit()
