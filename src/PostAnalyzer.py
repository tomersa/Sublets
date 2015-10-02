# -*- coding: utf-8 -*-

import re
import Entities
import Areas

class PostAnalyzer:
    __post_analyzer = None

    @staticmethod
    def create():
        if PostAnalyzer.__post_analyzer is None:
            PostAnalyzer.__post_analyzer = PostAnalyzer()

        return PostAnalyzer.__post_analyzer

    def __init__(self):
        self.__extractor = [PostAnalyzer.get_street]

    def analyze_post(self, post):
        analysis = {}
        for extractor in self.__extractor:
            analysis[extractor] = extractor(post.message)

        return Entities.AnalyzedPost(post, analysis)

    @staticmethod
    def get_numbers(message):
        return re.findall("\\d+", message)

    @staticmethod
    def get_street(message):
        match_object = re.search(u'רחוב (\W\W*?) ', message)
        if not match_object is None:
            a = match_object.groups(1)
            return match_object.groups(1)

        return u''

    @staticmethod
    def get_area(message):
        for area in Areas.Areas.get_areas():
            words = Areas.Areas.get_area_words(area)

            if not type(words) is type(()) and not type(words) is type([]):
                words = [words]

            for word in words:
                if word in message:
                    return area

        return u'' #No area
