# -*- coding: utf-8 -*-

class Areas:
    OLD_NORTH = "OLD_NORTH"
    BASEL = "BASEL"
    SHAPIRA = "SHAPIRA"
    FLORENTIN = "FLORENTIN"
    TEL_AVIV_CENTER = "TEL_AVIV_CENTER"
    DIZINGOFF_SQUARE = "DIZINGOFF_SQUARE"
    NACHALAT_BINYAMIN = "NACHALAT_BINYAMIN"
    KIKAR_RABIN = "KIKAR_RABIN"
    DIZINGOFF_CENTER = "DIZINGOFF_CENTER"
    RAMAT_AVIV = "RAMAT_AVIV"
    TAU = "TAU"
    YAFO = "YAFO"
    GAN_MEIR = "GAN_MEIR"
    BAVLI = "BAVLI"

    __AREAS = {OLD_NORTH: (u'צפון ישן', u'צפון הישן'),
               BASEL: (u'בזל'),
               BAVLI: (u'בבלי'),
               SHAPIRA: (u'שפירא'),
               FLORENTIN: (u'פלורנטין'),
               TEL_AVIV_CENTER: (u'מרכז תל אביב'),
               DIZINGOFF_SQUARE: (u'כיכר דיזינגוף' ,u' ככר דיזינגוף'),
               NACHALAT_BINYAMIN: (u'נחלת בנימין'),
               KIKAR_RABIN: (u'כיכר רבין' ,u' ככר רבין'),
               DIZINGOFF_CENTER: (u'דיזינגוף סנטר' ,u' הסנטר'),
               RAMAT_AVIV: (u'רמת אביב'),
               TAU: (u'אוניברסיטת תל אביב' ,u' אוניברסיטת ת"א'),
               YAFO: (u'יפו'),
               GAN_MEIR: (u'גן מאיר')}

    def __init__(self):
        pass

    @staticmethod
    def get_areas():
        return Areas.__AREAS.keys()

    @staticmethod
    def get_area_words(area):
        if area in Areas.__AREAS.keys():
            return Areas.__AREAS[area]

        return None