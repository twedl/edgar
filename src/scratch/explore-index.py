# download the index directory and explore it for future reference

import os
import gzip
import re
import lxml.etree as et
from urllib.request import urlopen, Request
import logging

import xmltodict, json
from bs4 import BeautifulSoup

edgar_index_re = re.compile(r"^http://www.sec.gov/(?:Archives|[Ii]ndexes.sec.gov)/edgar/(?P<schedule>full|daily)-index/(?P<year>[0-9]{4})/QTR(?P<qtr>[1-4])/sitemap\.(?P<name>.*\.xml)$")

def download_file(url, fname, force_update = False):
    """
    Download file from SEC/EDGAR database with appropriate headers
    # later: load UA from config

    If force_update is False and the file already exists,
        don't do anything. Similar to cache, but stored in a specific place.
    
    Input:
        - url: string; url from EDGAR API / www.sec.gov
        - fname: string; filename to store downloaded file
        - force_update: logical; if True, download the file even if it 
            already exists locally

    Output: 
        - None
    """

    if os.path.isfile(fname) is False or force_update is True:
        with urlopen(Request(
                url, 
                data = None, 
                headers = {
                        'User-Agent': 'Jesse Tweedle jesse.tweedle@gmail.com', 
                        'Accept-Encoding': 'gzip, deflate', 
                        'Host': 'www.sec.gov'
                    }
                )) as url_f:
            with open(fname, mode = "wb") as gz_f:
                gz_f.write(url_f.read())
                logging.info(f"File successfully downloaded to {fname}")
    else:
        logging.info(f"File alreaded downloaded to {fname}, re-run with force_update = True to overwrite file.")

    return None


def main():
    # do some things

    url = "https://www.sec.gov/Archives/edgar/daily-index/sitemap.xml"
    xml_fname = "data-scratch/sitemap.xml.gz"
    
    download_file(url, xml_fname)

    with open(xml_fname, mode = 'rb') as f:
        with gzip.open(f, mode = 'rb') as zip_ref:
            text = zip_ref.read()
    
    tree = et.ElementTree(et.fromstring(text))
    root = tree.getroot()

    index = []
    for child in root:
        index_url = child[1].text
        current_elem = {'url': index_url, 'last_modified': child[0].text}
        url_info = edgar_index_re.match(index_url)
        if url_info is not None:
            current_elem.update(url_info.groupdict())
            logging.info(f"Record parsed correctly: {index_url}")
        else: 
            logging.warning(f"Corrupt record: {url_info}")
        index.append(current_elem)
    
    # print(index[:2])

    # url = "https://www.sec.gov/Archives/edgar/daily-index/2017/QTR3/sitemap.20170803.xml"
    # fn = "data-scratch/sitemap.20170803.xml"
    # download_file(url, fn)

    # with open(xml_fname, mode = 'rb') as f:
    #     with gzip.open(f, mode = 'rb') as zip_ref:
    #         text = zip_ref.read()
    # print(text)
    
    # url = "http://www.sec.gov/Archives/edgar/data/1709660/9999999995-17-002008-index.htm"
    # ugh, that's a link to a html page that links the txt file
    # text file here:
    url = "https://www.sec.gov/Archives/edgar/data/1709660/999999999517002008/9999999995-17-002008.txt"
    fn = "data-scratch/9999999995-17-002008-index.txt.gz"
    download_file(url, fn)

    with open(fn, mode = 'rb') as f:
        with gzip.open(f, mode = 'rt') as zip_ref:
            text = zip_ref.read()
    # print(text) # but this isn't really xml; xml-ish



    # doc = xmltodict.parse(text)
    # print(json.dumps(doc))

    doc = BeautifulSoup(text, "lxml-xml")
    print(doc.prettify())

    # tree = et.ElementTree(et.fromstring(text))
    # print(str(tree))

    # tree = et.ElementTree(et.fromstring(text))
    # root = tree.getroot() 

    # alright, sick, amazing, now what
    # now look at an index itself?

if __name__ == "__main__":
    main()