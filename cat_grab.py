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

def download(url, out_folder):
    filename = url.split("/")[-1]
    filename = filename.split("?")[0]
    if filename == "":
        return 0
    outpath = os.path.join(out_folder, filename)
    if os.path.isfile(outpath): return 1
    try:
        urlretrieve(url, outpath)
    except:
        return 0
    print url + " > " + filename
    return 1

def openurl(url):
    headers = { 'User-Agent' : "Mozilla/5.0" }
    req = urllib2.Request(url, None, headers)
    try:
        htmlText = urllib2.urlopen(req).read()
    except:
        return ""
    return htmlText

def redditurl(url, out_folder, max_number):
    imgurregx = re.compile("http://imgur.com/\w+")
    aimgurregx = re.compile("http://imgur.com/a/\w+")   
    iimgurregx = re.compile("http://i.imgur.com/\w+")    
    default_image = re.compile("([^\s]+(\.(?i)(jpg|png|gif|bmp|jpeg|tif|tiff|emf|wmf))$)") 
    current_num = 0
    last = ""

    soup = bs(openurl(url))
    print "Page: " + url
    while int(current_num) < int(max_number):
        for link in soup.findAll("a"):
            try:
                href = str(link.get("href"))
            except:
                continue
            if last == href: continue
            if aimgurregx.match(href):
                page = openurl(href)
                if page == "": continue
                ssoup = bs(page)
                for img in ssoup.findAll(property="og:image"):
                    current_num += download(img.get("content"), out_folder)
            elif imgurregx.match(href):
                page = openurl(href)
                if page == "": continue
                ssoup = bs(page)
                try:
                    img = ssoup.find(rel="image_src").get("href")
                except:
                    continue
                current_num += download(img , out_folder)
            elif iimgurregx.match(href):
                current_num += download(href, out_folder)
            elif default_image.match(href):
                current_num += download(href, out_folder)
            last = href
        try:
            next_link = soup.find(rel="nofollow next").get("href")
        except:    
            return(-2)
        print "Next Page: " + next_link
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
    parser.add_argument("-n", "--number", required=False, help="Max number of pictures per URL. More of a guideline.", default="500", metavar="num")
    args = parser.parse_args()
    main(args.list, args.dir, args.number)
