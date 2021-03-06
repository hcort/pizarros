import pymongo

from pymongo import MongoClient

from podcast.db.dbcommons import BasicDB, PodcastEntry


class MongoDBPodcast(BasicDB):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['podcast-database']
        self.collection = self.db['podcast-database']
        self.collection.create_index("PodcastEntry.timestamp")

    def add_entry(self, podcast_entry: PodcastEntry) -> object:
        try:
            entry = self.encode_PodcastEntry(podcast_entry)
            self.collection.insert_one({"PodcastEntry": entry } )
            res = self.collection.count()
            return 1
        except Exception as ex:
            print(ex)
            return 0
    def remove_entry(self, podcast_entry ):
        self.collection.delete_one( podcast_entry )

    def get_entries(self, podcast_code: str):
        # important: specify the full json path to the field i want
        return self.collection.find({"PodcastEntry.podcast_code": podcast_code}).sort( "PodcastEntry.timestamp", pymongo.ASCENDING )

    def encode_PodcastEntry(self, podcast_entry):
        # converts a PodcastEntry to json
        return {"_type": "PodcastEntry",
                "timestamp": podcast_entry.timestamp,
                "mp3_link": podcast_entry.mp3_link,
                "entry_date": podcast_entry.entry_date,
                "entry_title": podcast_entry.entry_title,
                "mp3_filename": podcast_entry.mp3_filename,
                "podcast_title": podcast_entry.podcast_title,
                "podcast_code": podcast_entry.podcast_code }

    def decode_PodcastEntry(self, document):
        #res = document["PodcastEntry._type"]
        #res2 = document[_type]
        assert document["PodcastEntry"]["_type"] == "PodcastEntry"
        # transforms JSON to PodcastEntry
        return PodcastEntry(document[
                                "PodcastEntry"]["timestamp"],
                            document[
                                "PodcastEntry"]["mp3_link"],
                            document["PodcastEntry"]["entry_date"],
                            document["PodcastEntry"]["entry_title"],
                            document["PodcastEntry"]["mp3_filename"],
                            document["PodcastEntry"]["podcast_title"],
                            document["PodcastEntry"]["podcast_code"])
