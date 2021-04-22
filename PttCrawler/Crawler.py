
from network import CrawlerNetwork
import logging
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.DEBUG)

class Crawler(CrawlerNetwork):
    def __init__(self):
        super().__init__()
        self.baseHost = "https://www.ptt.cc"

    @staticmethod
    def doRegex(text, pattern):
        return re.findall(pattern, text)

    def getBoardAllArticleURL(self, url):
        text = self.httpGet(url)
        soup = BeautifulSoup(text, 'html.parser')
        res = soup.find_all(class_="r-ent")
        
        UrlList = []
        for item in res[1:]:
            r = self.doRegex(str(item), "<a href=\"(.+)\">")
            try:
                UrlList.append(r[0])
            except Exception as e:
                logging.error(e)
                exit(1)

        print(UrlList)
        return UrlList


    def getArticleComments(self, url):
        text = self.httpGet(url)
        
        soup = BeautifulSoup(text, 'html.parser')
        pushTag = soup.find_all(class_="f3 push-content")

        commentsList = [item.text for item in pushTag]
        for item in commentsList:
            logging.debug(item)

        return commentsList

    # def getArticle(self, url):
    #     text = self.httpGet(url)
    #     soup = BeautifulSoup(text, 'html.parser')

    #     r = soup.find(id="main-content")
    #     print(r.string)

if __name__ == "__main__":
    C = Crawler()
    #C.getArticleComments("https://www.ptt.cc/bbs/Gossiping/M.1619097885.A.79D.html")
    C.getBoardAllArticleURL("https://www.ptt.cc/bbs/Gossiping/index.html") #目前只能爬一頁