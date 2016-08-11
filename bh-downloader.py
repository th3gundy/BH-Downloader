# Yunus YILDIRIM

# -*- coding: utf-8 -*-

import requests
import os
from time import time as timer
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

# import for "'ascii' codec can't decode byte" error
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# import for "'ascii' codec can't decode byte" error

def linkCrawler(url):
    print "[+] Crawling started."

    urls = []
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all('a', class_='link-icon')
    for href in a:
            urls.append(href["href"])
    print "[+] Crawling done."
    print '[+] Total URLs Crawled : ' + str(len(urls))
    return urls


def fileDownloader(link):
    local_filename = link.split('/')[-1][6:]

    try:
        print "[+] Download started for: " + str(link)
        r = requests.get(link, stream=True)
        with open(local_filename, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print "[+] Download finished for: " + str(link)
    except Exception as e:
        print "[!] Failed to download file: " + str(link) + " error: " + str(e)


def main(main_url):

    year = main_url.split("/")[3].upper()

    directoryName = "BlackHat-%s-Documents" %(year)
    if not os.path.exists(directoryName):
            os.mkdir(directoryName)
    os.chdir(directoryName)

    links = linkCrawler(main_url)

    pool = ThreadPool(8)
    pool.map(fileDownloader, links)


if len(sys.argv) != 2:
    print "[!] Missing parameters"
    print "[+] Usage: python %s Brifieng_url" %(sys.argv[0])
    print "[+] Ex: python %s https://www.blackhat.com/us-16/briefings.html" %(sys.argv[0])
else:
    print "[+] Starting.."

    start = timer()
    main(sys.argv[1])

    print 'Script Execution Time : %s sec' % (timer() - start)
