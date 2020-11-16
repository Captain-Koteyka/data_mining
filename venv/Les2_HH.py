from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

profession = 'кузнец'
main_link = 'https://hh.ru/search/vacancy'
params = {'L_save_area': 'true',
          'clusters': 'true',
          'enable_snippets': 'true',
          'search_field': 'name',
          'text': profession,
          'showClusters': 'true'
          }
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
response = requests.get(main_link, params=params, headers=headers)
all_vacancies = []
dom = bs(response.text, 'html.parser')
vacancy_list = dom.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
while True:
    for vacancy in vacancy_list:
        vacancy_data = {}
        info = vacancy.find('a')
        name = info.text
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary is None:
            pass
        else:
            salary = salary.text.split()
            currency = salary[-1]
            salary.pop()
            salary_new = ' '.join(salary)
            if 'бел.' in salary_new:
                salary_new = salary_new[:-4]
                currency = 'бел. руб.'
            if 'от' in salary_new:
                salary_min = None
                salary_max = int(salary_new[3:].replace(' ', ''))
            elif 'до' in salary_new:
                salary_min = int(salary_new[3:].replace(' ', ''))
                salary_max = None
            else:
                salary_new = salary_new.split('-')
                salary_min = int(salary_new[0].replace(' ', ''))
                salary_max = int(salary_new[1].replace(' ', ''))
        vacancy_link = info['href']
        website = 'https://hh.ru'
        vacancy_data['name'] = name
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['currency'] = currency
        vacancy_data['vacancy_link'] = vacancy_link
        vacancy_data[' website'] = website
        all_vacancies.append(vacancy_data)
    if dom.find(text='дальше'):
        text = dom.find(text='дальше')
        next_link = website + text.parent['href']
        response = requests.get(next_link, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancy_list = dom.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    else:
        break

#df = pd.DataFrame(all_vacancies)
print(df)
