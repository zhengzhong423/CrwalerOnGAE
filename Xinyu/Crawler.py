from MajeCrawler import *
from SandroCrawler import *


class Crawler(object):
    @staticmethod
    def go():
        MajeCrawl().crawl()
        SandroCrawl().crawl()

if __name__ == '__main__':
    Crawler().go()
