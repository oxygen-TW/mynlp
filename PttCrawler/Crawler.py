from network import CrawlerNetwork
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

class Crawler(CrawlerNetwork):
    def __init__(self):
        super().__init__()

    def getArticleComments(self, url):
        text = self.httpGet(url)
        
        soup = BeautifulSoup(text, 'html.parser')
        pushTag = soup.find_all(class_="f3 push-content")

        commentsList = [item.text for item in pushTag]
        for item in commentsList:
            logging.debug(item)

        return commentsList

if __name__ == "__main__":
    C = Crawler()
    C.getArticleComments("https://www.ptt.cc/bbs/Gossiping/M.1619097885.A.79D.html")