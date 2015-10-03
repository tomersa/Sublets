# -*- coding: utf-8 -*-

import codecs
import re
import Entities
import Areas

class PostAnalyzer:
    __post_analyzer = None

    __DAYS_IN_TYPICAL_MONTH = 30

    @staticmethod
    def create():
        if PostAnalyzer.__post_analyzer is None:
            PostAnalyzer.__post_analyzer = PostAnalyzer()

        return PostAnalyzer.__post_analyzer

    def __init__(self):
        self.__extractor = [self.get_price]

        with codecs.open("res/tel_aviv_streets", "r", encoding='utf-8') as f:
            self.__streets = f.read().splitlines()

    def analyze_post(self, post):
        analysis = {}
        for extractor in self.__extractor:
            analysis[extractor] = extractor(post.message)

        return Entities.AnalyzedPost(post, analysis)

    def get_price(self, message):
        # 3,200 ש"ח
        prices = re.findall(u'(\d+(?:,\d+)*)(?: *ש"ח)', message)

        if len(prices) > 0:
            return int(prices[0].replace(u',', u''))

        # 3,200 ₪
        prices = re.findall(u'(\d+(?:,\d+)*)(?: *₪)', message)

        if len(prices) > 0:
            return int(prices[0].replace(u',', u''))

        #2000 שקלים
        prices = re.findall(u'(\d+(?:,\d+)*)(?: *שקל)', message)

        if len(prices) > 0:
            return int(prices[0].replace(u',', u''))

        # 2000 לחודש
        prices = re.findall(u"(\d+(?:,\d+)*) לחודש", message)
        if len(prices) > 0:
            return int(prices[0].replace(u',', u''))

        #150 ללילה,
        prices = re.findall(u"(\d+(?:,\d+)*) ללילה", message)
        if len(prices) > 0:
            return int(prices[0].replace(u',', u'')) * PostAnalyzer.__DAYS_IN_TYPICAL_MONTH

    #Assuming line starts with the street name
    def __get_valid_street_name(self, line):
        possible_streets = filter(line.startswith, self.__streets)

        if len(possible_streets) is 0:
            return None

        longest = max(map(len, possible_streets))

        for street in possible_streets:
            if len(street) is longest:
                return street

        raise StandardError("Couldn't find longest street(That's logically impossible).")


    def get_street(self, message):
        match_object = re.search(u'רחוב (\W\W*?) ', message)
        if not match_object is None:
            return self.__get_valid_street_name(match_object.groups()[0])

        return u''

    def get_area(self, message):
        for area in Areas.Areas.get_areas():
            words = Areas.Areas.get_area_words(area)

            if not type(words) is type(()) and not type(words) is type([]):
                words = [words]

            for word in words:
                if word in message:
                    return area

        return u'' #No area
