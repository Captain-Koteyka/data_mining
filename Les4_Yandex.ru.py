from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
main_link = 'https://yandex.ru/news/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
news = dom.xpath("//h2[@class='news-card__title']/../..")
news_list = []
for n in news[:5]:
    news_dict = {}
    source_name = n.xpath(".//span[@class='mg-card-source__source']/a/text()")
    name = n.xpath(".//h2[@class='news-card__title']/text()")
    links = n.xpath(".//h2[@class='news-card__title']/../@href")
    publication_time = n.xpath(".//span[@class='mg-card-source__time']/text()")

    news_dict['source_name'] = source_name[0]
    news_dict['name'] = name[0]
    news_dict['links'] = links[0]
    news_dict['publication_time'] = publication_time[0]

    news_list.append(news_dict)
pprint(news_list)
client = MongoClient('127.0.0.1', 27017)
db = client['Yandex.ru_news']
news_collection = db.news_collection
news_collection.insert_many(news_list)