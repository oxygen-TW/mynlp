import requests
from bs4 import BeautifulSoup

class CrawlerNetwork():

    def __init__(self):
        self.pttBaseUrl = "https://www.ptt.cc/bbs/Gossiping/index.html/"
        self.cookies = {"over18":"1"}

    def httpGet(self, url, timeoutSec=5):
        res = requests.get(url, cookies=self.cookies, timeout=timeoutSec)

        if(res.status_code != 200):
            raise CrawlerCanNotFetch
        
        return res.text

class CrawlerCanNotFetch(Exception):
    pass

if __name__ == "__main__":
    N = CrawlerNetwork()
    r = N.httpGet("https://www.pttweb.cc/bbs/Gossiping")
    print(r)