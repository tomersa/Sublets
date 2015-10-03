# -*- coding: utf-8 -*-
import codecs
import os

import unittest
from PostAnalyzer import PostAnalyzer
from DataReceiver import DataReceiver


class PostAnalyzerTest(unittest.TestCase):
    @staticmethod
    def get_received_data():
        return DataReceiver("res/sublet_in_telaviv_for_short_periods").get_data()

    #Testing case: 3,200 ש"ח
    def test_price_1(self):
        price = 4000
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[60]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

        price = 2500
        analyzed = PostAnalyzer.create().analyze_post(received_data[61]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

    #Testing case: 2000 לחודש
    def test_price_2(self):
        price = 5700
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[3]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))


if __name__ == '__main__':
    unittest.main()

# #
# 3,200 ש״ח
# 2000 לחודש -
# 150 ללילה,
# 2000₪
# מחיר 2000 שקלים כולל חשבונות !
# 2000 ש"ח לכל התקופה
# 3500 ש״ח כולל הכל
# 2800 ש״ח לחודש כולל הכל
# כל חדר זמין ב-1600 ש"ח לחודש כולל כל החשבונות
# ,1900שקל לכל התקופה כולל חשבונות
# ₪3200  שכ״ד חודשי כולל כל החשבונות.
#
#
#
# \d(!?,\d)
# #