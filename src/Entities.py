import re
import os

class Post:
    def __init__(self, json_post):
        self.id = json_post[u'id']
        self.message = json_post[u'message']
        self.updated_time = json_post[u'updated_time']

def get_numbers(message):
    return re.findall("\\d+", message)

class AnalyzedPost:
    __filters = [get_numbers]

    def __init__(self, post):
        self.__analysis = {}
        self.__post = post

        for filter in AnalyzedPost.__filters:
            self.__analysis[filter] = filter(self.__post.message)

    def __str__(self):
        return str(self.__analysis.values())