import scrapy
from scrapy.http import HtmlResponse
from goods_for_repair.items import GoodsForRepairItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath("//a[@slot='name']")

        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodsForRepairItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_xpath('unit', "//span[@slot='unit']/text()")
        loader.add_xpath('characteristic_name', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('characteristic_value', "//dd[@class='def-list__definition']/text()")
        loader.add_value('characteristics', {})
        loader.add_value('link', response.url)

        yield loader.load_item()
