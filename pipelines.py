# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class GoodsForRepairPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        item['characteristics'] = dict(zip(item['characteristic_name'], item['characteristic_value']))
        collection = self.mongo_base[spider.name]
        #collection.insert_one(item)
        collection.insert_one({'name': item['name'], 'photos': item['photos'], 'price': item['price'],
                               'currency': item['currency'], 'unit': item['unit'], 'link': item['link'],
                               'characteristics': item['characteristics']})
        return item


class LeroyMerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            print()
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        #return item



    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        name_folder = item['name']
        file = request.url.split('/')[-1]
        file_name = file.split('.')[0]
        file_extension = file.split('.')[1]
        return f'{name_folder}/{file_name}.{file_extension}'
