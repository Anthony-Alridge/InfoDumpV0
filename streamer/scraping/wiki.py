import wikipedia


class Wiki():

    def __init__(self, topic):
        self.topic = topic

    def summarise(self):
        default_summary = "Sorry we couldn't generate a summary for that one, write your own with the text editor and save as summary.txt"
        try:
            summary = wikipedia.summary(self.topic)
            return summary
        except:
            return default_summary

    def get_url(self):
        url = wikipedia.url(self.topic)
        return url
