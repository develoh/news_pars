import json

with open("news.json", encoding='UTF-8') as file:
    news_dict = json.load(file)

search_url = 'https://news.rambler.ru/world/52365646-sholts-poobeschal-bystro-rassledovat-situatsiyu-vokrug-zapisi-razgovora-ofitserov-frg/'

if search_url in news_dict:
    print('Новость есть уже')
else:
    print('Новости нет еще')