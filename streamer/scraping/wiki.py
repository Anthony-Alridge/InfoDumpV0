import wikipedia


class Wiki():

    def __init__(self, topic):
        self.topic = topic

    def summarise(self):
        summary = wikipedia.summary(self.topic)
        return summary

    def get_url(self):
        url = wikipedia.url(self.topic)
        return url