import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BD%D0%B0%D1%83%D0%BA%D0%B0']

    def parse(self, response: HtmlResponse):

        book_links = response.xpath("//a[@class='book-preview__title-link']/@href").extract()
        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath("//*[normalize-space(text()) = 'Далее']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='item-detail__title']/text()").extract_first()
        author = response.xpath("//a[@itemprop='author']//text()").extract()
        basic_price = response.xpath("//div[@class='item-actions__price-old']//text()").extract()
        discounted_price = response.xpath("//b[@itemprop='price']//text()").extract()
        link = response.xpath("//link[@rel='amphtml']/@href").extract()
        rating = response.xpath("//span[@class='rating__rate-value']//text()").extract()
        yield BookparserItem(
            item_name=name, item_author=author, item_basic_price=basic_price, item_discounted_price=discounted_price,
            item_link=link, item_rating=rating)
