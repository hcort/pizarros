import collections


class PodcastEntry(object):
    # basic information
    # link to mp3
    # date
    # title
    # podcast title

    def __init__(self):
        # what do I have to do?
        pass

    def __init__(self, link, date, title, podcast_tit, podcast_cod ):
        self.mp3_link = link
        self.entry_date = date
        self.entry_title = title
        self.podcast_title = podcast_tit
        self.podcast_code = podcast_cod



class BasicDB:
    # does nothing at all!
    def add_entry(self, PodcastEntry ):
        pass

    def get_entries(self, podcast):
        pass