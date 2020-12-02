from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from goods_for_repair import settings
from goods_for_repair.spiders.leroymerlin import LeroymerlinSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search='напольная плитка')

    process.start()
