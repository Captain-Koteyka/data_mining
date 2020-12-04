# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    name = scrapy.Field()
    user_id = scrapy.Field()
    photo = scrapy.Field()
    parse_user = scrapy.Field()
    category = scrapy.Field()
    _id = scrapy.Field()
