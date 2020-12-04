import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    insta_login = 'train1234567890'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1607021461:AflQAAq7CXIBwtkkmrzYyIdDz772B7Zz/CoKHPUArNmRYNJCSkX6kzdh8o0NIjPDJcWlhdF7r9WKievk79V1y1CKp2Cq64Rdzq1GlW7j+/XirZko1Q5kJMqkTlg/zWdp17vHIT0xpEQn0xWDiw=='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = 'hamovniki_tribe'

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    subscribers_hash = 'c76146de99bb02f6415203be841dd25a'
    subscriptions_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def user_data_parse(self, response: HtmlResponse, username, parse_user):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'include_reel': True,
                     'fetch_mutual': False,
                     'first': 12}
        url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
        url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
        yield response.follow(
            url_subscribers,
            callback=self.user_subscribers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'parse_user': parse_user,
                       'variables': deepcopy(variables)}
        )
        yield response.follow(
            url_subscriptions,
            callback=self.user_subscriptions_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'parse_user': parse_user,
                       'variables': deepcopy(variables)}
        )

    def user_subscribers_parse(self, response: HtmlResponse, username, user_id, variables, parse_user):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscribers,
                callback=self.user_subscribers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'parse_user': parse_user,
                           'variables': deepcopy(variables)}
            )
        subscribers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for subscriber in subscribers:
            item = InstaparserItem(
                name=subscriber['node']['username'],
                user_id=subscriber['node']['id'],
                photo=subscriber['node']['profile_pic_url'],
                parse_user=parse_user,
                category='subscribers'
            )
        yield item

    def user_subscriptions_parse(self, response: HtmlResponse, username, user_id, variables, parse_user):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'
            yield response.follow(
                url_subscriptions,
                callback=self.user_subscriptions_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'parse_user': parse_user,
                           'variables': deepcopy(variables)}
            )
        subscriptions = j_data.get('data').get('user').get('edge_follow').get('edges')
        for subscription in subscriptions:
            item = InstaparserItem(
                name=subscription['node']['username'],
                user_id=subscription['node']['id'],
                photo=subscription['node']['profile_pic_url'],
                parse_user=parse_user,
                category='subscriptions'
            )
        yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
