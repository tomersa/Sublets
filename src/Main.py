import os
import sys
import codecs

from DataReceiver import DataReceiver
from PostAnalyzer import PostAnalyzer

DEBUG = True

class Sublets:
    def __init__(self, group_feed_directory):
        self.__dr = DataReceiver(group_feed_directory)
        self.__anaylzed_posts = []

        if not os.path.exists("output"):
            os.makedirs("output")

        if not os.path.exists("output/analyzed"):
            os.makedirs("output/analyzed")

    def main(self):

        recieved_data = self.__dr.get_data()

        if DEBUG:
            recieved_data = recieved_data

        for post in recieved_data:
            with codecs.open(os.path.join("output", post.id), "w", encoding='utf-8') as out:
                out.write(post.message)

            analyzed = PostAnalyzer.create().analyze_post(post)

            with codecs.open(os.path.join("output/analyzed", post.id), "w", encoding='utf-8') as out:
                out.write(unicode(analyzed))

            print analyzed

if __name__ == "__main__":
    group_feed_directory = sys.argv[1]
    sublets = Sublets(group_feed_directory)
    sublets.main()
