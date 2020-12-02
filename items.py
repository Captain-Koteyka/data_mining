# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def change_photo_url(url):
    if url:
        url = url.replace('w_82,h_82', 'w_1200,h_1200')
    return url


def price_transform(price):
    return float(''.join(price.split()))


def characteristic_value_transform(value):
    return ''.join(value.split())

class GoodsForRepairItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_photo_url))
    price = scrapy.Field(input_processor=MapCompose(price_transform), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    characteristic_name = scrapy.Field()
    characteristic_value = scrapy.Field(input_processor=MapCompose(characteristic_value_transform))
    characteristics = scrapy.Field()
    _id = scrapy.Field()
