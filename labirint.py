import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BD%D0%B0%D1%83%D0%BA%D0%B0/?stype=0']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath("//a[@class='product-title-link']/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath(
            "//div[@class='pagination-next']/a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//a[@data-event-label='author']//text()").extract()
        basic_price = response.xpath("//span[@class='buying-priceold-val-number']//text()").extract()
        discounted_price = response.xpath("//span[@class='buying-pricenew-val-number']//text()").extract()
        link = response.xpath("//link[@rel='canonical']/@href").extract()
        rating = response.xpath("//div[@id='rate']//text()").extract()
        yield BookparserItem(
            item_name=name, item_author=author, item_basic_price=basic_price, item_discounted_price=discounted_price,
            item_link=link, item_rating=rating)
