import urllib.request


class PodcastDownloader:

    def __init__(self, podcast_cod, database ):
        self.podcast_code = podcast_cod
        self.db = database

    def start_batch_download(self):
        # I´ll iterate through the db collection and download
        # each podcast
        # get the entries for the given code
        items = self.db.get_entries( self.podcast_code )
        res = items.count()
        for item in items:
            entry = self.db.decode_PodcastEntry( item )
            #print( entry.mp3_link)
            self.get_mp3_file( entry )

    def get_mp3_file( self, entry ):
        dat = ""
        req = urllib.request.Request(entry.mp3_link)
        with urllib.request.urlopen(req) as response:
            data = response.read()
        #req2 = urllib.request( entry.mp3_link )
        #response = urllib.urlopen(req2)
        # grab the data
        #data = response.read()
        mp3Name = entry.entry_title + ".mp3"
        song = open(mp3Name, "wb")
        song.write(data)  # was data2
        song.close()
