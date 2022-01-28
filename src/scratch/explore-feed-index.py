# explore the feed / index.json

import json
import os
import gzip
import re
# import lxml.etree as et
from urllib.request import urlopen, Request
import time
import logging
from pathlib import Path
import urllib.parse

# import xmltodict, json
# from bs4 import BeautifulSoup

base_url = "https://www.sec.gov/Archives/edgar"

def download_index(url, fname, force_update = False):
    if os.path.isfile(fname) is False or force_update is True:
        time.sleep(1) # one request per second, just in case
        with urlopen(Request(
                url, 
                data = None, 
                headers = {
                        'User-Agent': 'Jesse Tweedle jesse.tweedle@gmail.com', 
                        'Accept-Encoding': 'gzip, deflate', 
                        'Host': 'www.sec.gov'
                    }
                )) as url_f:
            # make directory if it doesn't exist already
            with open(fname, mode = "wb") as gz_f:
                gz_f.write(url_f.read())
                logging.info(f"File successfully downloaded to {fname}")
    else:
        logging.info(f"File alreaded downloaded to {fname}, re-run with force_update = True to overwrite file.")

    return None

def url_to_name(url, type):
    return os.path.join("data-scratch", type, re.sub(r"/", "-", url.lower()) + ".gz")

def main():

    # url = "https://www.sec.gov/Archives/edgar/Feed/index.json"
    base_url = "https://www.sec.gov/Archives/edgar"
    base_index = "Feed/index.json"
    # scratch_dir = "data-scratch"
    # url = os.path.join(base_url, index_json)
    url = f"{base_url}/{base_index}"
    # print(url)

    # fname = "data-scratch/feed-index.json"
    # fname = re.sub("\/", "-", index_json.lower()) + ".gz"
    fname = url_to_name(index_json, type = "index")
    # print(fname)

    download_index(url, fname)
    # download_index(url, os.path.join(index_json, ".gz"))

    with open(fname, mode = 'rb') as f:
        with gzip.open(f, mode = 'rb') as zip_ref:
            text = zip_ref.read()
        
    index = json.loads(text)

    # so...download all the index files? or download all the jsons, stack them all together?
    # ...how to keep track of the last modified thing?
    # print(json.dumps(index["directory"], indent = 2, sort_keys = True))

    json_stack = [index]
    # instead:
    # json_stack = [(url, fname)]
    while json_stack:
        current = json_stack.pop()["directory"]
        for item in current["item"]:
            next_name = f"{current['name']}{item['href']}index.json"
            next_url = f"{base_url}/{next_name}"
            # if item["type"] == "dir":
            #   type = "index"
            # elif item["type"] == "file":
            #   type = "file"
            download_index(next_url, url_to_name(next_name, type = "index"))
            # print(next_name)
            # break


if __name__ == "__main__":
    main()