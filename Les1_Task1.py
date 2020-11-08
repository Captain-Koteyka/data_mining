import requests
import json

user_name = 'Captain-Koteyka'
main_link = 'https://api.github.com/users'
repos_link = main_link + '/' + user_name + '/repos'
response = requests.get(repos_link)
j_data = response.json()
with open('j_data.json', 'w') as outfile:
    json.dump(j_data, outfile)
print(f"Список репозиториев пользователя {user_name}: ")
for i in j_data:
    print(i['name'])
