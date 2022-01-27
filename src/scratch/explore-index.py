# download the index directory and explore it for future reference

import os
import gzip
import re
import lxml.etree as et
from urllib.request import urlopen, Request
import logging

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
    
    print(index[:2])
    # alright, sick, amazing, now what
    # now look at an index itself?

if __name__ == "__main__":
    main()