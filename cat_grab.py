"""
cat_grab.py
    Downloads all images from a text file of line delimeted URLs.
    
    Usage: python cat_grab.py cat_list.txt
"""
from bs4 import BeautifulSoup as bs
import urlparse
import os
import sys
import urllib2
from urllib import urlretrieve
import re
import time
import uuid

def download(url, out_folder):
    filename = url.split("/")[-1]
    filename = filename.split("?")[0]
    if filename == "":
        filename = str(uuid.uuid4())
    outpath = os.path.join(out_folder, filename)
    urlretrieve(url, outpath)
    print filename

def openurl(url):
    headers = { 'User-Agent' : "Mozilla/5.0" }
    req = urllib2.Request(url, None, headers)
    htmlText = urllib2.urlopen(req).read()
    return htmlText

def redditurl(url, out_folder, max_number):
    imgurregx = re.compile("http://imgur.com/")
    aimgurregx = re.compile("http://imgur.com/a/")   
    iimgurregx = re.compile("http://i.imgur.com/")    
    current_num = 0
    last = ""
    soup = bs(openurl(url))
    while current_num < max_number:
        for link in soup.findAll("a"):
            try:
                href = str(link.get("href"))
            except:
                continue
            if last == href: continue
            if aimgurregx.match(href):
                print "album!"
                ssoup = bs(openurl(href))
                for img in ssoup.findAll(property="og:image"):
                    download(img.get("content"), out_folder)
                print "end"
            elif imgurregx.match(href):
                ssoup = bs(openurl(href))
                download(ssoup.find(rel="image_src").get("href"), out_folder)
                current_num += 1
            elif iimgurregx.match(href):
                download(href, out_folder)
                current_num += 1
            last = href
        try:
            next_link = soup.find(rel="nofollow next").get("href")
        except:    
            return(-2)
        print next_link
        soup = bs(openurl(next_link))

def genericurl(url, out_folder, max_number):
    soup = bs(openurl(url))
    for image in soup.findAll("img"):
        print ("Image: " + (image.get("src")))
        download(image.get("src"))

def main(url_file, out_folder, max_number):
    """Downloads all the images at 'url' to cats/"""
    with open(url_file) as u_file:
        url_list = u_file.readlines()
    redditreg = re.compile('http://reddit.com/r/')
    for url in url_list:
        if redditreg.match(url) :
            redditurl(url, out_folder, max_number)
        else:
            genericurl(url, out_folder, max_number)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="For downloading lots and lots of cat pictures.")
    parser.add_argument('list', help="Line delimeted file of URLs")
    parser.add_argument('-d', "--dir", required=False, help="Dir to download to", default='./Cats', metavar="dir")
    #parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-n", "--number", required=False, help="Max number of pictures per URL", default="500", metavar="num")
    args = parser.parse_args()
    main(args.list, args.dir, args.number)