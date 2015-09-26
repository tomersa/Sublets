import os
import sys
import codecs
import json
import pprint

DEBUG = True

#
class UnicodePrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
#

class DataReceiver:
    def __init__(self, group_feed_directory):
        self.__message_queue = []

        if not os.path.exists(group_feed_directory):
            raise Exception("group feed directory doesn't exist: {0}".format(group_feed_directory))

        if DEBUG:
            for file in os.listdir(group_feed_directory)[:1]:
                group_feed_file = os.path.join(group_feed_directory, file)

                with codecs.open(group_feed_file, "r", encoding="utf-8") as gf_handle:
                    data = json.load(gf_handle)
                    UnicodePrettyPrinter().pprint(data['data'][0])

        else:
            for file in os.listdir(group_feed_directory):
                group_feed_file = os.path.join(group_feed_directory, file)

                with codecs.open(group_feed_file, "r", encoding="utf-8") as gf_handle:
                    data = json.load(gf_handle)
                    pprint(data)

    def get_data(self):
        return 0





class Sublets:
    def __init__(self, group_feed_directory):
        self.__dr = DataReceiver(group_feed_directory)

    def main(self):
        pass

if __name__ == "__main__":
    group_feed_directory = sys.argv[1]
    sublets = Sublets(group_feed_directory)
    sublets.main()