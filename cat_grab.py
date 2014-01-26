"""
cat_grab.py
    Downloads all images from a specified URL.
"""
from bs4 import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import sys

def main(ur;, out_folder="/Users/nbeede7/Cats"):
    """Downloads all the images at 'url' to /Users/nbeede7/Cats"""
    soup = bs(urlopen(url))
    parsed = list(urlparse.urlparse(url))