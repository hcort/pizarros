import urllib

from os.path import isfile
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3

#   write tags using pytag
#       doesn´t have support for cover art
# def write_mp3_tags( entry, mp3_name):
#     # put some ID3 tags into the mp3 file
#     try:
#         audio = AudioReader(mp3_name)
#         tags = audio.get_tags()
#         print(tags)
#         # title
#         # artist
#         # album
#         # date
#         # tracknumber (???)
#         newtags = {'title': entry.entry_title, 'artist': entry.podcast_title, 'date': entry.entry_date}
#         audio.write_tags(newtags)
#     except FormatNotSupportedError:
#         print('Process other file...')
#     pass

# downloads, if needed, the cover art for the podcast
#   then, it adds it as an ID3 tag
def write_cover_art(entry, mp3_name ):
    cover_name = "C:\\Users\\Héctor\\Downloads\\melodias_pizarras\\" + entry.podcast_code + ".png"
    if isfile(cover_name) == False:
        # download cover art
        cover_url = "http://img.rtve.es/p/" + entry.podcast_code + "/"
        req = urllib.request.Request( cover_url )
        cover_file = open(cover_name, "ba")
        with urllib.request.urlopen(cover_url) as response:
            buffer = response.read()
            cover_file.write(buffer)
            cover_file.close()
    # put some ID3 tags into the mp3 file
    audio = MP3(mp3_name, ID3=ID3)
    # add ID3 tag if it doesn't exist
    try:
        audio.add_tags()
    except Exception as ex:
        pass
    try:
        file = open(cover_name, 'rb')
        data = file.read()
        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/png',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=data
            )
        )
    except Exception as ex:
        pass
    audio.save()

# writes some basic ID3 tags to the mp3 file
def write_mp3_tags( entry, mp3_name):
    write_cover_art(entry, mp3_name)
    audio = EasyID3(mp3_name)
    audio["title"] = entry.entry_title
    audio["artist"] = entry.podcast_title
    audio["album"] = entry.podcast_title
    audio["date"] = entry.entry_date
    audio.save()