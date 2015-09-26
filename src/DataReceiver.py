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
    ERROR_COULDNT_READ_MESSAGE = "couldn't process post"
    ERROR_COULDNT_READ_JSON = "Couldn't read json"

    def __init__(self, group_feed_directory):
        self.__post_queue = []
        self.__errors = {DataReceiver.ERROR_COULDNT_READ_MESSAGE:0, DataReceiver.ERROR_COULDNT_READ_JSON:0}

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
                    self.__errors[DataReceiver.ERROR_COULDNT_READ_JSON] += 1
                    data = None
                    continue

                for post in data['data']:
                    try:
                        self.__post_queue.append(Post(post))
                    except StandardError:
                        self.__errors[DataReceiver.ERROR_COULDNT_READ_MESSAGE] += 1

        for error_message, times in self.__errors.items():
            if times > 0:
                print "{0} {1} times".format(error_message, times)

    def get_data(self):
        return self.__post_queue