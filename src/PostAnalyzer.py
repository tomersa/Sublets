# -*- coding: utf-8 -*-

import codecs
import re
import Entities
import Areas

class PostAnalyzer:
    __post_analyzer = None

    __DAYS_IN_TYPICAL_MONTH = 30

    __PRICE_REGEXES = (u'(\d+(?:,\d+)*)(?: *ש"ח)', u'(\d+(?:,\d+)*)(?: *ש\u05f4{0,1}ח)',u'(\d+(?:,\d+)*)(?: *כולל)', u'(\d+(?:,\d+)*)(?: *₪)', u'(\d+(?:,\d+)*)(?: *שקל)', u"(\d+(?:,\d+)*) לחודש",\
                       u"משכירים ב\-{0,1}(\d+(?:,\d+)*)", u'(\d+(?:,\d+)*)(?: *לכל התקופה)', u"המחיר:{0,1} (\d+(?:,\d+)*)", u"המחיר לכל התקופה הוא (\d+(?:,\d+)*)", u"שכר דירה (\d+(?:,\d+)*)", u"שכ\"{0,1}ד (\d+(?:,\d+)*)", u"שכ\u05f4{0,1}ד (\d+(?:,\d+)*)",\
                       u"להשכרה ב\-{0,1}(\d+(?:,\d+)*)", u"whole period is (\d+(?:,\d+)*)", u"(\d+(?:,\d+)*) EUR per", u"(\d+(?:,\d+)*) [Ss]hekel", u'(\d+(?:,\d+)*)(?: *לחודש)', u'(\d+(?:,\d+)*)(?: *NIS)',\
                       u'(\d+(?:,\d+)*)(?: *Nis)', u'ONLY (\d+(?:,\d+)*)', u'only (\d+(?:,\d+)*)', u'(\d+(?:,\d+)*)(?: *ils)', u'(\d+(?:,\d+)*)(?: *לא כולל)', u'(\d+(?:,\d+)*)(?: *INS)', u'\n(\d+(?:,\d+)*)\n')

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
        for regex in PostAnalyzer.__PRICE_REGEXES:
            prices = re.findall(regex, message)

            if len(prices) > 0:
                return int(prices[0].replace(u',', u''))

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
