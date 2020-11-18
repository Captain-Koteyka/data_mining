from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
main_link = 'https://news.mail.ru/inregions/moscow/90/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
links = dom.xpath('//span[@class="photo__title photo__title_new photo__title_new_hidden js-topnews__notification"]/../../@href')[:3]
links2 = dom.xpath('//a[@class="list__text"]/@href')[:6]
for link in links2:
    links.append(link)
news_list = []
for link in links:
    main_link = link
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news_dict = {}

    name = dom.xpath("//h1[@class='hdr__inner']/text()")
    publication_date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    source_name = dom.xpath("//span[@class='breadcrumbs__item']/span[@class='note']/a[@class='link color_gray breadcrumbs__link']/span[@class='link__text']/text()")

    news_dict['source_name'] = source_name
    news_dict['name'] = name[0]
    news_dict['links'] = main_link
    news_dict['publication_date'] = publication_date[0].split('T')[0]

    news_list.append(news_dict)
pprint(news_list)
client = MongoClient('127.0.0.1', 27017)
db = client['Mail.ru_news']
news_collection = db.news_collection
news_collection.insert_many(news_list)
