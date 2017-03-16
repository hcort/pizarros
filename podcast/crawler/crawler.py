import requests
from requests import RequestException
# regular expressions
import re
# beautiful soup for HTML parsing
from bs4 import BeautifulSoup

def start_crawl(podcastCode):
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
    start_point = start_point.replace("__%2__", podcastCode)
    while (current_page != last_index):
        # build the url
        current = start_point.replace("__%1__", str(current_page))
        # get the page
        try:
            page = requests.get(current)
            if (page.status_code != requests.codes.ok):
                break
            if 0 == last_index:
                last_url = re.compile('href=\"(.+)\"><span>Último')
                try:
                    found = re.search(last_url, page.text).group(1)
                    last_num = re.compile('pbq=(\d+)&')
                    found = re.search(last_num, found).group(1)
                    last_index = int(found)
                except AttributeError:
                    break
            # gather all links
            print( "\n\nPágina " + str(current_page) + " de " + str(last_index) )
            soup = BeautifulSoup(page.text)
            # all the download links are in a table with odd and even rows
            # from this table I´ll get the links and info about each file
            all_odds = soup.findAll("li", {"class": "odd"})
            all_even = soup.findAll("li", {"class": "even"})
            # merge both sets
            all_items = all_odds + all_even
            # i´m going to use this a lot
            href_regex = re.compile('href=\"(.*)\"')
            i = 0
            for item in all_items:
                # mp3 link in span col_tip
                mp3_link = item.find( "span", { "class": "col_tip"})
                #mp3_link = re.search( href_regex, mp3_link.contents[1]).group(1)
                mp3_link = mp3_link.contents[1].attrs["href"]
                title = item.find( "span", { "class": "titulo-tooltip"})
                title_as_link = title.contents[0].attrs["href"]
                print( "\t" + str(i) + "\t" + title.contents[0].attrs["title"] + ": " + title_as_link + " -> " + mp3_link )
                i += 1
            current_page += 1
        except RequestException as ex:  # this covers everything
            print("Couldn´t get page" + current)
            break
