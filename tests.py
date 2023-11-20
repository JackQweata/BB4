import unittest
from utils.codeforces import CodeforcesApi


class TestCodeforcesApi(unittest.TestCase):
    """ Тестирования запросов к сайту """

    def setUp(self):
        self.initializer = CodeforcesApi()

    def test_parsing(self):
        result = self.initializer.task_parsing()
        self.assertIsInstance(result, list)

    def test_tags(self):
        result = self.initializer.get_tags_on_site()
        self.assertIsInstance(result, dict)
