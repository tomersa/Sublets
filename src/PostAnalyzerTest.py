# -*- coding: utf-8 -*-
import unittest
from PostAnalyzer import PostAnalyzer
from DataReceiver import DataReceiver


class PostAnalyzerTest(unittest.TestCase):
    @staticmethod
    def get_received_data():
        return DataReceiver("res/sublet_in_telaviv_for_short_periods").get_data()

    def setUp(self):
        PostAnalyzer.create().set_extractors("GET_PRICE")

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

    #1450 כולל הכל
    def test_price_3(self):
        price = 1450
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[913]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

    # 3,200 ₪
    def test_price_4(self):
        price = 1500
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[11]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

    # 2000 שקלים
    def test_price_5(self):
        price = 445
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[365]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

    # משכירים ב-
    def test_price_6(self):
        price = 3800
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[0]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

    # משכירים ב-
    def test_price_7(self):
        price = 3500
        received_data = PostAnalyzerTest.get_received_data()
        analyzed = PostAnalyzer.create().analyze_post(received_data[1]).get_analysis().values()[0]
        self.assertEqual(analyzed, price, "Couldn't match price {0} (got: {1})".format(price, analyzed))

    def test_price_all_prices_no_exception(self):
        received_data = PostAnalyzerTest.get_received_data()

        for i in received_data:
            PostAnalyzer.create().analyze_post(i).get_analysis().values()[0]

if __name__ == '__main__':
    unittest.main()
