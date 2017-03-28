

import requests
from requests import RequestException
# regular expressions
import re
# beautiful soup for HTML parsing
from bs4 import BeautifulSoup
# to create the date of each program
from datetime import date

from podcast.db.dbcommons import PodcastEntry




class PodcastCrawler:

    def __init__(self, podcast_cod, database ):
        self.podcast_code = podcast_cod
        self.podcast_title = ""
        self.db = database


    def start_crawl(self ):
        # gather the start point URL
        # in pbq I put the page number
        # in ctx I put the code that identifies the program I want to download
        start_point = "http://www.rtve.es/alacarta/interno/contenttable.shtml?" \
                      "pbq=__%1__&" \
                      "orderCriteria=DESC&modl=TOC&locale=es&pageSize=15" \
                      "&ctx=__%2__&typeFilter=39816"
        # first page
        current_page = 1
        # get last page from the "Último" link
        #   get the whole link
        #   <a name="paginaIR" href="..."><span>Último</span></a>
        #   get the number from the pbq field
        #
        last_index = 0
        get_more_pages = 1
        start_point = start_point.replace("__%2__", self.podcast_code)
        while current_page != last_index:
            # build the url
            current = start_point.replace("__%1__", str(current_page))
            # get the page
            try:
                page = requests.get(current)
                if page.status_code != requests.codes.ok:
                    break
                # in the first iteration I don´t know the number of pages
                if 0 == last_index:
                    try:
                        last_index = self.get_last_page(page)
                    except AttributeError:
                        break
                print("\n\nPágina " + str(current_page) + " de " + str(last_index))
                self.parse_html(page)
                current_page += 1
            except RequestException as ex:  # this covers everything
                print("Couldn´t get page" + current)
                break


    def get_last_page( self, page: requests.Response) -> int:
        last_url = re.compile('href=\"(.+)\"><span>Último')
        found = re.search(last_url, page.text).group(1)
        last_num = re.compile('pbq=(\d+)&')
        found = re.search(last_num, found).group(1)
        index = int(found)
        return index


    def get_podcast_title(self,soup):
        # the podcast title is in the h2 node
        h2 = soup.find("h2")
        try:
            self.podcast_title = h2.text
            title_rgx = re.compile('Completos de (.+)\n')
            return re.search(title_rgx, self.podcast_title).group(1)
        except:
            # do nothing
            return ""


    def parse_html(self,page: requests.Response) -> None:
        # gather all links
        soup = BeautifulSoup(page.text)
        if self.podcast_title == "" :
            self.podcast_title = self.get_podcast_title(soup)
        # all the download links are in a table with odd and even rows
        # from this table I´ll get the links and info about each file
        all_odds = soup.findAll("li", {"class": "odd"})
        all_even = soup.findAll("li", {"class": "even"})
        # merge both sets
        all_items = all_odds + all_even
        self.parse_list_items(all_items )


    def parse_list_items(self, all_items: object ) -> None:
        i = 0
        for item in all_items:
            # mp3 link in span col_tip
            try:
                mp3_link = item.find("span", {"class": "col_tip"})
                # mp3_link = re.search( href_regex, mp3_link.contents[1]).group(1)
                mp3_link = mp3_link.contents[1].attrs["href"]
                title = item.find("span", {"class": "titulo-tooltip"})
                title_as_link = title.contents[0].attrs["href"]
                plain_title = title.contents[0].attrs["title"]
                print(self.podcast_title + "\t" + str(i) + "\t" + plain_title + ": " + title_as_link + " -> " + mp3_link)
                entry = self.create_entry( mp3_link, title_as_link, plain_title )
                if entry is not None:
                    self.db.add_entry( entry )
            except Exception as ex:
                # do nothing?
                print(ex)
                print("Bad parsing in item " + str(i))
            i += 1

    def create_entry(self, mp3_link, title_as_link, plain_title):
        title_split = title_as_link.split('/')
        # split format for Radio 3 podcasts
        # / alacarta / audio / podcast-title / podcast-title-entry-title-date
        # entry-title may be empty!!!!
        try:
            prog_date = ""
            date_rgx = re.compile("-([0-9]{2})-([0-9]{2})-([0-9]{2})$")
            found = re.search(date_rgx, title_split[4])
            if found is not None:
                day = found.group(1)
                month = found.group(2)
                year = found.group(3)
                prog_date = date(int(year)+2000, int(month), int(day))
                prog_date_str = str( prog_date )
            else:
                # another date format
                date_rgx = re.compile("-([0-9]{2})([0-9]{2})([0-9]{2})$")
                found = re.search(date_rgx, title_split[4])
                if found is not None:
                    day = found.group(1)
                    month = found.group(2)
                    year = found.group(3)
                    prog_date = date(int(year)+2000, int(month), int(day))
                    prog_date_str = str( prog_date )

            mp3_filename = title_split[3] + "-" + prog_date_str
            title = ""
            if plain_title == "":
                title = mp3_filename
            else:
                title = plain_title[+4:]
            entry = PodcastEntry(mp3_link, prog_date_str, title, mp3_filename, self.podcast_title, self.podcast_code)
            return entry
        except Exception as ex:
            print( ex )
            return None
