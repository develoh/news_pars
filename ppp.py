import json
import requests
from bs4 import BeautifulSoup


def get_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

    url = 'https://news.rambler.ru/world/?ysclid=lt9yq2rskv519849782'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    cards = soup.find_all('a', class_='_1uRkW')

    news_dict = {}
    for article in cards:
        article_title = article.get('aria-label')
        # print(article_title)
        article_cat = article.find('div', class_='_2Cd-1').find('div', class_='_2vif1').text
        # print(article_cat)
        article_data = article.find('span').text
        # print(article_data)
        article_image_url = article.find('img', class_='_3hvpU').get('src').split('&')[0]
        # print(article_image_url)
        article_url = article.get("href")
        news_dict[article_url] = {
            'article_title': str(article_title).replace('\xa0', ' '),
            'article_cat': article_cat,
            'article_data': article_data,
            'article_image_url': article_image_url,
            'article_url': article_url
        }
        with open('news.json', 'w', encoding='UTF-8') as f:
            json.dump(news_dict, f, indent=4, ensure_ascii=False)


def check_new_updates():
    with open("news.json", encoding='UTF-8') as file:
        news_dict = json.load(file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

    url = 'https://news.rambler.ru/world/?ysclid=lt9yq2rskv519849782'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.find_all('a', class_='_1uRkW')

    fresh_news = {}

    for article in cards:

        article_url = article.get("href")

        if article_url in news_dict:
            continue
        else:
            article_title = article.get('aria-label')
            article_cat = article.find('div', class_='_2Cd-1').find('div', class_='_2vif1').text
            article_data = article.find('span').text
            article_image_url = article.find('img', class_='_3hvpU').get('src').split('&')[0]

            news_dict[article_url] = {
                'article_title': str(article_title).replace('\xa0', ' '),
                'article_cat': article_cat,
                'article_data': article_data,
                'article_image_url': article_image_url,
                'article_url': article_url
            }

            fresh_news[article_url] = {
                'article_title': str(article_title).replace('\xa0', ' '),
                'article_cat': article_cat,
                'article_data': article_data,
                'article_image_url': article_image_url,
                'article_url': article_url
            }

    with open('news.json', 'w', encoding='UTF-8') as f:
        json.dump(news_dict, f, indent=4, ensure_ascii=False)

    return fresh_news
def main():
    print(check_new_updates())


if __name__ == '__main__':
    main()
