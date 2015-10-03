class Post:
    def __init__(self, json_post):
        self.id = json_post[u'id']
        self.message = json_post[u'message']
        self.updated_time = json_post[u'updated_time']


class AnalyzedPost:
    def __init__(self, post, analysis):
        self.__analysis = analysis
        self.__post = post

    def __str__(self):
        return str(self.__analysis)

    def get_analysis(self):
        return dict(self.__analysis)