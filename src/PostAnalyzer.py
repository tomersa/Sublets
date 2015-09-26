import re
import Entities

class PostAnalyzer:
    __post_analyzer = None

    @staticmethod
    def create():
        if PostAnalyzer.__post_analyzer is None:
            PostAnalyzer.__post_analyzer = PostAnalyzer()

        return PostAnalyzer.__post_analyzer

    def __init__(self):
        self.__filters = [PostAnalyzer.get_numbers]

    def analyze_post(self, post):
        analysis = {}
        for filter in self.__filters:
            analysis[filter] = filter(post.message)

        return Entities.AnalyzedPost(post, analysis)

    @staticmethod
    def get_numbers(message):
        return re.findall("\\d+", message)