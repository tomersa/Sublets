# -*- coding: utf-8 -*-

import codecs
import re
import Entities
import Areas
import calendar


class PostAnalyzer:
    __post_analyzer = None

    __DAYS_IN_TYPICAL_MONTH = 30

    __PRICE_REGEXES = (u'(\d+(?:,\d+)*)(?: *ש"ח)', u'(\d+(?:,\d+)*)(?: *ש\u05f4{0,1}ח)', u'(\d+(?:,\d+)*)(?: *כולל)',
                       u'(\d+(?:,\d+)*)(?: *₪)', u'(\d+(?:,\d+)*)(?: *שקל)', u"(\d+(?:,\d+)*) לחודש", \
                       u"משכירים ב\-{0,1}(\d+(?:,\d+)*)", u'(\d+(?:,\d+)*)(?: *לכל התקופה)',
                       u"המחיר:{0,1} (\d+(?:,\d+)*)", u"המחיר לכל התקופה הוא (\d+(?:,\d+)*)",
                       u"שכר דירה (\d+(?:,\d+)*)", u"שכ\"{0,1}ד (\d+(?:,\d+)*)", u"שכ\u05f4{0,1}ד (\d+(?:,\d+)*)", \
                       u"להשכרה ב\-{0,1}(\d+(?:,\d+)*)", u"whole period is (\d+(?:,\d+)*)", u"(\d+(?:,\d+)*) EUR per",
                       u"(\d+(?:,\d+)*) [Ss]hekel", u'(\d+(?:,\d+)*)(?: *לחודש)', u'(\d+(?:,\d+)*)(?: *NIS)', \
                       u'(\d+(?:,\d+)*)(?: *Nis)', u'ONLY (\d+(?:,\d+)*)', u'only (\d+(?:,\d+)*)',
                       u'(\d+(?:,\d+)*)(?: *ils)', u'(\d+(?:,\d+)*)(?: *לא כולל)', u'(\d+(?:,\d+)*)(?: *INS)',
                       u'\n(\d+(?:,\d+)*)\n')

    EXTRACTORS = None

    @staticmethod
    def create():
        if PostAnalyzer.__post_analyzer is None:
            PostAnalyzer.__post_analyzer = PostAnalyzer()

        return PostAnalyzer.__post_analyzer

    def __init__(self):
        PostAnalyzer.EXTRACTORS = {"GET_PHONE": self.get_phone, "GET_PRICE": self.get_price,
                                   "GET_PRICE_PERIOD": self.get_price_period, "GET_STREET": self.get_street,
                                   "GET_AREA": self.get_area}

        self.__extractor = []
        self.set_extractors("GET_PRICE_PERIOD")

        with codecs.open("res/tel_aviv_streets", "r", encoding='utf-8') as f:
            self.__streets = f.read().splitlines()

        self.__months = [month for month in calendar.month_name]
        self.__months.extend((
            u'ינואר', u'פברואר', u'מרץ', u'אפריל', u'מאי', u'יוני', u'יולי', u'אוגוסט', u'ספטמבר', u'אוקטובר',
            u'נובמבר',
            u'דצמבר'))

    def set_extractors(self, *methods):
        self.__extractor = [PostAnalyzer.EXTRACTORS[method] for method in methods]

    def analyze_post(self, post):
        analysis = {}
        for extractor in self.__extractor:
            analysis[extractor.__name__] = extractor(post.message)

        return Entities.AnalyzedPost(post, analysis)

    def get_phone(self, message):
        phones = re.findall(u'\d{3}\-\d{7}', message)

        if len(phones) > 0:
            return phones[0]

        return None

    def get_price(self, message):
        for regex in PostAnalyzer.__PRICE_REGEXES:
            prices = re.findall(regex, message)

            if len(prices) > 0:
                return int(prices[0].replace(u',', u''))

        prices = re.findall(u"(\d+(?:,\d+)*) ללילה", message)

        if len(prices) > 0:
            return int(prices[0].replace(u',', u'')) * PostAnalyzer.__DAYS_IN_TYPICAL_MONTH

        return None

    def get_price_period(self, message):
        period = re.findall(u'[pP]er [Nn]ight|PER NIGHT|\d+ {0,1}[\\u05f4₪]{0,1}\/ night|ללילה', message)

        if len(period) > 0:
            return "PER_NIGHT"

        period = re.findall(u'[pP]er [Mm]onth|PER MONTH\d+ {0,1}[\\u05f4₪]{0,1}\/ month|לחודש', message)

        if len(period) > 0:
            return "PER_MONTH"

        period = re.findall(u'[Ee]ntire [Pp]eriod|לכל התקופה', message)

        if len(period) > 0:
            return "PER_ENTIRE_PERIOD"

        # Trying getting numerical date.
        for reg in (u'\d+\/\d+\-\d+\/\d+|\d+\.\d+\-\d+\.\d+', u''):
            period = re.findall(reg, message)

            if not len(period) is 1:
                continue

            period = set(re.findall(u'\d+/\d+|\d+\.\d+', period[0]))

        if len(period) is 2:
            return period

        # Trying to get written date
        month_indices = [(re.search(unicode(month), message).start(), month) for month in self.__months if
                         not re.search(unicode(month), message) is None]
        min_index, min_month = month_indices[0]
        for index, month in month_indices:
            if index < min_index:
                min_index = index
                min_month = month

        #TODO: Continue finding the other month by name, convert to numerical and return.
        return None

    # Assuming line starts with the street name
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

        return None

    def get_area(self, message):
        for area in Areas.Areas.get_areas():
            words = Areas.Areas.get_area_words(area)

            if not type(words) is type(()) and not type(words) is type([]):
                words = [words]

            for word in words:
                if word in message:
                    return area

        return None  # No area
