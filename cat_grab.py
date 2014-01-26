"""
cat_grab.py
    Downloads all images from a text file of line delimeted URLs.
    
    Usage: python cat_grab.py cat_list.txt
"""
from bs4 import BeautifulSoup as bs
import urlparse, os, sys
from urllib2 import urlopen
from urllib import urlretrieve

def main(url_file, out_folder="/Users/nbeede7/Cats"):
    """Downloads all the images at 'url' to /cats/"""
    with open(url_file) as u_file:
        url_list = u_file.readlines()
        
    for url in url_list:
        soup = bs(urlopen(url))
        url_parsed = list(urlparse.urlparse(url))
        
        for image in soup.findAll("img"):
            print "Image: " + (image["src"])
            filename = image["src"].split("/")[-1]
            url_parsed[2] = image["src"]
            outpath = os.path.join(out_folder, filename)
            if image["src"].lower().startswith("http"):
                urlretrieve(image["src"], outpath)
            else:
                urlretrieve(urlparse.urlunparse(parsed), outpath)
    
if __name__ == "__main__":
    url_file = sys.argv[-1]
    out_folder = "/Users/nbeede7/Cats"
    main(url_file, out_folder)