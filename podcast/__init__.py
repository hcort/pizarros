import pprint

import podcast.crawler
from podcast.crawler.crawler import PodcastCrawler
from podcast.db.mongo import MongoDBPodcast
from podcast.downloader.downloader import PodcastDownloader


def main() :
    db = MongoDBPodcast()
    podcast_code = "22332"
    crawl = PodcastCrawler(podcast_code,db)
 #   result = db.collection.delete_many({"PodcastEntry.podcast_code": podcast_code})
    items = db.get_entries(podcast_code)
    res = items.count()
    crawl.start_crawl( )
    download = PodcastDownloader(podcast_code,db)
    download.start_batch_download()



if __name__ == "__main__" : main()