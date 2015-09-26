import sys
import pprint

from src.DataReceiver import DataReceiver


DEBUG = True

#
class UnicodePrettyPrinter(pprint.PrettyPrinter):
    def format(self, raw_object, context, max_levels, level):
        if isinstance(raw_object, unicode):
            return raw_object.encode('utf8'), True, False

        return pprint.PrettyPrinter.format(self, raw_object, context, max_levels, level)


#

class Post:
    def __init__(self, json_post):
        self.id = json_post[u'id']
        self.message = json_post[u'message']
        self.updated_time = json_post[u'updated_time']


class Sublets:
    def __init__(self, group_feed_directory):
        self.__dr = DataReceiver(group_feed_directory)

    def main(self):
        for post in self.__dr.get_data():
            print post.message

if __name__ == "__main__":
    group_feed_directory = sys.argv[1]
    sublets = Sublets(group_feed_directory)
    sublets.main()