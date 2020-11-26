# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    item_name = scrapy.Field()
    item_author = scrapy.Field()
    item_basic_price = scrapy.Field()
    item_discounted_price = scrapy.Field()
    item_link = scrapy.Field()
    item_rating = scrapy.Field()
    _id = scrapy.Field()


