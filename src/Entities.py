__author__ = 'tomer'


class Post:
    def __init__(self, json_post):
        self.id = json_post[u'id']
        self.message = json_post[u'message']
        self.updated_time = json_post[u'updated_time']