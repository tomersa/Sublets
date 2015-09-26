import os
import sys
import codecs

from DataReceiver import DataReceiver
from Entities import AnalyzedPost

class Sublets:
    def __init__(self, group_feed_directory):
        self.__dr = DataReceiver(group_feed_directory)
        self.__anaylzed_posts = []

        os.makedirs("output")

    def main(self):
        for post in self.__dr.get_data():
            with codecs.open(os.path.join("output", post.id), "w", encoding='utf-8') as out:
                out.write(post.message)

            analyzed = AnalyzedPost(post)

            print analyzed

if __name__ == "__main__":
    group_feed_directory = sys.argv[1]
    sublets = Sublets(group_feed_directory)
    sublets.main()