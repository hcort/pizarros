import urllib.request

from podcast.downloader.taghelper import write_mp3_tags


class PodcastDownloader:
    def __init__(self, podcast_cod, database):
        self.podcast_code = podcast_cod
        self.db = database

    # gets the result set from the database
    # iterates the result list and downloads each file
    def start_batch_download(self):
        # I´ll iterate through the db collection and download
        # each podcast
        # get the entries for the given code
        items = self.db.get_entries(self.podcast_code)
        res = items.count()
        for item in items:
            entry = self.db.decode_PodcastEntry(item)
            print( entry.timestamp + "\t" + entry.entry_date + "\t" + entry.podcast_title )
            #if self.get_mp3_file(entry) == True:
            #   self.db.remove_entry(item)


    # downloads the mp3 file using urllib
    def get_mp3_file(self, entry):
        dat = ""
        req = urllib.request.Request(entry.mp3_link)
        mp3_name = "C:\\Users\\Héctor\\Downloads\\melodias_pizarras\\" + entry.mp3_filename + ".mp3"
        song = open(mp3_name, "ba")
        # download the file in chunks
        # (only to print progress for debug purposes)
        with urllib.request.urlopen(req) as response:
            total_size = response.getheader('Content-Length')
            #total_size = response.info().getheader('Content-Length').strip()
            total_size = int(total_size)
            total_mb = total_size / 1024 /1024
            bytes_so_far = 0
            print( "Starting download: " + entry.mp3_link)
            #data = response.read()
            chunk_size = 1024*1024*10 # 10 mbs/chunk
            while 1:
                chunk = response.read(chunk_size)
                song.write(chunk)  # was data2
                bytes_so_far += len(chunk)
                print( "Downloaded " + str( bytes_so_far/1024/1024) + " of " + str(total_mb ))
                if not chunk:
                    break
                #if report_hook:
                #    report_hook(bytes_so_far, chunk_size, total_size)
        song.close()
        # add some ID3 tags
        write_mp3_tags(entry, mp3_name)
        return True
