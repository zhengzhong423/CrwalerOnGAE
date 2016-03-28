from MajeCrawler import *
from SandroCrawler import *


class Crawler(object):
    def go(self):
        MajeCrawl().crawl()
        SandroCrawl().crawl()

if __name__ == '__main__':
    Crawler().go()
