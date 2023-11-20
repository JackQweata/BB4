import requests
from bs4 import BeautifulSoup
from config import SITE_DOMAIN


class CodeforcesApi:
    def __init__(self):
        self.__headers = {"Accept-Language": "ru,en;q=0.9,pt;q=0.8"}

    def task_parsing(self):
        """  Парсинг задач """

        response = requests.get(f"{SITE_DOMAIN}api/problemset.problems", headers=self.__headers)

        if response.status_code != 200:
            return

        result = response.json()['result']
        russifier = self.get_tags_on_site()

        for problem in result['problems']:
            problem['tags'] = [russifier.get(item, item) for item in problem['tags']]

            for stat in result['problemStatistics']:
                if problem["contestId"] == stat["contestId"] and problem["index"] == stat["index"]:
                    problem["solvedCount"] = stat["solvedCount"]
                    break

        return result['problems']

    def get_tags_on_site(self) -> dict:
        """ Парсинг тега с сайта """

        site = requests.get(f"{SITE_DOMAIN}problemset", headers=self.__headers)

        soup = BeautifulSoup(site.text, "html.parser")

        tags_label = soup.find('label', class_='_FilterByTagsFrame_addTagLabel')
        tags_options = tags_label.findAll('option')

        tags = {}
        for item in tags_options:
            if item.get("value") is None or item.get('title') is None:
                continue
            tags[item["value"]] = item["title"]

        return tags
