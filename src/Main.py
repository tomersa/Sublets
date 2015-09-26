import os
import sys
import codecs
import json
import pprint

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

class DataReceiver:
    def __init__(self, group_feed_directory):
        self.__post_queue = []

        self.read_feed(group_feed_directory)

    def read_feed(self, group_feed_directory):
        if not os.path.exists(group_feed_directory):
            raise Exception("group feed directory doesn't exist: {0}".format(group_feed_directory))

        file_list = os.listdir(group_feed_directory)

        if DEBUG:
            file_list = file_list[:1]

        for file in file_list:
            group_feed_file = os.path.join(group_feed_directory, file)

            with codecs.open(group_feed_file, "r", encoding="utf-8") as gf_handle:
                data = json.load(gf_handle)
                UnicodePrettyPrinter().pprint(data['data'][0])
                for post in data['data']:
                    try:
                        self.__post_queue.append(Post(post))
                    except Exception:
                        print "couldn\'t process post"

    def get_data(self):
        return self.__post_queue


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