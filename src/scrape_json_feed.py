# explore the feed / index.json

import shutil
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
import tarfile
# import xmltodict, json
# from bs4 import BeautifulSoup

base_url = "https://www.sec.gov/Archives/edgar/"

def download_archive(url, fname, force_update = False):
    if Path(fname).exists() is False or force_update is True:
        time.sleep(1) # two requests per second, just in case
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
            # print(url_f.read())
            Path(fname.parent).mkdir(parents=True, exist_ok=True)
            with open(fname, mode = "wb") as tar_f:
                shutil.copyfileobj(url_f, tar_f)
                logging.info(f"File successfully download to {fname}")
    else:
        logging.info(f"File alreaded downloaded to {fname}, re-run with force_update = True to overwrite file.")

    return None


def download_index(url, fname, force_update = False):
    if Path(fname).exists() is False or force_update is True:
        time.sleep(1) # two requests per second, just in case
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
            Path(fname.parent).mkdir(parents=True, exist_ok=True)
            with open(fname, mode = "wb") as gz_f:
                shutil.copyfileobj(url_f, gz_f)
                # gz_f.write(url_f.read())
                logging.info(f"File successfully downloaded to {fname}")
    else:
        logging.info(f"File alreaded downloaded to {fname}, re-run with force_update = True to overwrite file.")

    return None

def open_index(fname):
    """
    Input: index.json.gz filename
    Output: parsed index json
    """
    # with open(fname, mode = 'rb') as f:
    # with gzip.open(f, mode = 'rb') as zip_ref:
    with gzip.open(fname, mode = 'rb') as zip_ref:
        return json.loads(zip_ref.read())

def remove_suffixes(fname):
    fname = fname.with_suffix("")
    while fname.suffix != "":
        fname = fname.with_suffix("")
    return fname

def open_nc_archive(fname, dir_name):
    """     
    Unpack and re-zip each file?
    Input: YYYYMMDD.nc.tar.gz filename
    Output: list of SGML objects/text?
    """
    with tarfile.open(fname, mode = 'r:gz') as tar_ref:
        dir_name.mkdir(parents = True, exist_ok = True)
        tar_ref.extractall(path = dir_name)

def re_zip_archive(dir_name):
    """
    """
    for file in dir_name.iterdir():
        if file.suffix == ".gz": # skip files that are already done by a previous run;
            # they should be overwritten by this step later
            continue
        file_gz = file.with_suffix(file.suffix + ".gz")
        # print(file.with_suffix(file.suffix + ".gz")) # could be .nc or .corr01
        with open(file, mode = "rb") as f_in:
            with gzip.open(file_gz, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # then delete file
        Path.unlink(file)
        # break
        # with file.open() as f:
            # with gzip
    # list all the files in dir_name
    # for each file, zip it, then remove current one
    
        # print(fname)
        # print(remove_suffixes(fname))
        # x = tar_ref.getmember('./0001209191-22-005399.nc')
        # print(x[:5])
        # nc_file = x#[0]
        # handle = tar_ref.extractfile(nc_file)
        # open a gz file, write this info to it
        # with gzip.open(_____, mode = "w|gz") as gz_f:
            # print(handle.read())
        # basically, 


def get_links_from_index(index):
    # index object has directory, which has [item, name, parent-dir]
    # need name for url and fname
    # parent-dir is nothing
    # in item, a list of items
    # return list of tuples: (url, fname)
    directory = index["directory"]
    dir_name = directory["name"]
    items = directory["item"]

    links = []

    for item in items:
        href = item["href"]
        if item["type"] == "dir":
            url = "".join([base_url, dir_name, href, "index.json"])
            fname = Path("data-scratch", dir_name, href, "index.json.gz")
        elif item["type"] == "file":
            url = "".join([base_url, dir_name, href])
            fname = Path("data-scratch", dir_name, href)
        else:
            logging.info(f"Link {href} type is {item['type']}, not 'dir' or 'file'; skipping")
            continue
        links.append((url, fname))
        
    return links



def main():

    base_index = ["Feed/", "index.json"]
    url = ''.join([base_url, *base_index])
    fname = Path("data-scratch", *base_index).with_suffix(".json.gz")

    index_stack = [(url, fname)]

    while index_stack:
        url, fname = index_stack.pop()
        # first, skip nc.tar.gz files:
        # if str(fname)[-7:] == ".tar.gz":
        # if str(url)[-10:] != "index.json": 
        if fname.suffixes == [".nc", ".tar", ".gz"]: # fname must be Path that ends in ".nc.tar.gz"
            # alright, next, gacefully take care of files that aren't .tar.gz; e.g., 2012/QTR3/ one file ends in .nc
            # print((url, fname))
            download_archive(url, fname)
            print(f"trying archive {url}")
            dir_name = remove_suffixes(fname)
            # huh, this is tougher than just passing the directory through
            open_nc_archive(fname, dir_name)
            re_zip_archive(dir_name)
            # then delete the fname too? maybe later
        elif fname.suffixes == [".json", ".gz"]:
            print(f"downloading {fname}")
            download_index(url, fname)
            current = open_index(fname)
            links = get_links_from_index(current)
            index_stack.extend(links)

    # uh I think that's it. see how much that is. see how complex that is anyway
    # remove directories if they already exist?
if __name__ == "__main__":
    main()