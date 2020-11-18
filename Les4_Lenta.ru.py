from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
news = dom.xpath("//time[@class='g-time']/..")
news_list = []
for n in news:
    n_dict = {}
    source_name = 'lenta.ru'
    name = n.xpath(".//time[@class='g-time']/../text()")
    links = n.xpath(".//time[@class='g-time']/../@href")
    publication_date = n.xpath(".//time[@class='g-time']/@datetime")

    n_dict['source_name'] = source_name
    n_dict['name'] = name[0].replace('\xa0', ' ')
    n_dict['links'] = source_name + links[0]
    n_dict['publication_date'] = publication_date[0]

    news_list.append(n_dict)
pprint(news_list)
client = MongoClient('127.0.0.1', 27017)
db = client['Lenta.ru_news']
news_collection = db.news_collection
news_collection.insert_many(news_list)
