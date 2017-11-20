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

    def __init__(self, timestamp, link, date, title, filename, podcast_tit, podcast_cod ):
        self.timestamp = timestamp
        self.mp3_link = link
        self.entry_date = date
        self.entry_title = title
        self.mp3_filename = filename
        self.podcast_title = podcast_tit
        self.podcast_code = podcast_cod



class BasicDB:
    # does nothing at all!
    def add_entry(self, PodcastEntry ):
        pass

    def get_entries(self, podcast):
        pass
