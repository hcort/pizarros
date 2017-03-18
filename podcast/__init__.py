import pprint

import podcast.crawler
from podcast.crawler.crawler import PodcastCrawler
from podcast.db.mongo import MongoDBPodcast


def main() :
    db = MongoDBPodcast()
    crawl = PodcastCrawler("22332",db)
    crawl.start_crawl( )
    items = db.get_entries( "22332")
    res = items.count()
    for item in items:
        #pprint.pprint(item)
        entry = db.decode_PodcastEntry( item )
        print( entry.mp3_link)


if __name__ == "__main__" : main()