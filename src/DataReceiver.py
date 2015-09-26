import types
import pprint
import codecs
import json
import os

from Entities import Post


class UnicodePrettyPrinter(pprint.PrettyPrinter):
    def format(self, raw_object, context, max_levels, level):
        if isinstance(raw_object, unicode):
            return raw_object.encode('utf8'), True, False

        return pprint.PrettyPrinter.format(self, raw_object, context, max_levels, level)


class DataReceiver:
    ERROR_COULDNT_READ_MESSAGE = "Unprocessed posts"
    ERROR_COULDNT_READ_JSON = "Non readable json file: {0}"
    JSONS_READ = "JSONs read"
    POSTS_READ = "Posts read"

    def __init__(self, group_feed_directory):
        self.__post_queue = []
        self.__statistics = {DataReceiver.ERROR_COULDNT_READ_MESSAGE: 0, DataReceiver.ERROR_COULDNT_READ_JSON: [],
                             DataReceiver.JSONS_READ: 0, DataReceiver.POSTS_READ: 0}

        self.read_feed(group_feed_directory)

    def read_feed(self, group_feed_directory):
        if not os.path.exists(group_feed_directory):
            raise Exception("group feed directory doesn't exist: {0}".format(group_feed_directory))

        file_list = os.listdir(group_feed_directory)

        if os.path.exists(".debug"):
            file_list = file_list[:1]

        for file in file_list:
            group_feed_file = os.path.join(group_feed_directory, file)

            with codecs.open(group_feed_file, "r", encoding="utf-8") as gf_handle:
                data = None
                try:
                    data = json.load(gf_handle)
                except StandardError, e:
                    self.__statistics[DataReceiver.ERROR_COULDNT_READ_JSON].append(
                        DataReceiver.ERROR_COULDNT_READ_JSON.format(file))
                    continue

                self.__statistics[DataReceiver.JSONS_READ] += 1

                for post in data['data']:
                    try:
                        self.__post_queue.append(Post(post))
                    except StandardError:
                        self.__statistics[DataReceiver.ERROR_COULDNT_READ_MESSAGE] += 1

                    self.__statistics[DataReceiver.POSTS_READ] += 1

        for stat_name, stat_value in self.__statistics.items():
            if type(stat_value) is type([]) and len(stat_value) > 0:
                for value in stat_value:
                    print value

            elif stat_value > 0:
                print "{0}: {1}".format(stat_name, stat_value)

    def get_data(self):
        return self.__post_queue