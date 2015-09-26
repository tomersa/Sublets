import sys
import codecs

from DataReceiver import DataReceiver

class Sublets:
    def __init__(self, group_feed_directory):
        self.__dr = DataReceiver(group_feed_directory)

    def main(self):
        for post in self.__dr.get_data():
            with codecs.open(post.id, "w", encoding='utf-8') as out:
                out.write(post.message)

if __name__ == "__main__":
    group_feed_directory = sys.argv[1]
    sublets = Sublets(group_feed_directory)
    sublets.main()