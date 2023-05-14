import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
import os
import dotenv

# Загрузка настроек из файла .env
from dotenv import load_dotenv
load_dotenv()

last_page = 3

base_url = "https://coinmarketcap.com/"
firms_data = []

# Получение учетных данных прокси-сервера из переменных окружения
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

# Указание настроек прокси-сервера
PROXY_HOST = "zproxy.lum-superproxy.io"
PROXY_PORT = "22225"

# Создание сессии
session = requests.Session()
session.verify = False
session.proxies = {
    'http': f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
    'https': f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
}

# Отключение проверки SSL-сертификатов
# requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Создаем список для хранения всех ссылок на врачей
all_coin_links = []





def get_html(url):
    # Загружаем страницу
    response = session.get(url)
    # print(response)
    # Ожидание загрузки страницы
    time.sleep(10)
    return response.text

def get_all_links(html):
    # Получение HTML-кода страницы с результатами поиска
    soup = BeautifulSoup(html, 'html.parser')
    out = soup.find('table', class_='sc-beb003d5-3')
    links = out.find_all('a', class_='cmc-link')
    links_all = [urljoin(base_url, link.get('href', '')) for link in links]
    return links_all


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        name = soup.find('h1', class_='base-text').text.strip()
    except:
        name = 'No name data'
    try:
        price_div = soup.find('div', class_='alignBaseline')
        price = price_div.find('span', class_='base-text').text.strip()
    except:
        name = 'No price data'
    data = { 'name': name, 'price': price}
    return data

# Сохраняем результаты в CSV-файл
def write_csv(data):
    with open('coin_price_data.csv', 'a', newline='', encoding='utf-8') as file:
        # fieldnames = ['Name', 'Description', 'Website', 'LinkedIn']
        writer = csv.writer(file)
        # writer.writeheader()
        # for firm_data in firms_data:
        writer.writerow( (counter, data['name'], data['price'] ))
        print( data['name'] )


def main():
    start = datetime.now()
    page = 1
    # Создаем глобальный счетчик
    counter = 1
    while True:
        # Формируем ссылку на текущую страницу
        url = f'https://coinmarketcap.com/' if page == 1 else f'https://coinmarketcap.com/?page={page}'
        html = get_html(url)
        all_coin_links = get_all_links(html)
        print('PAGE=>', page, all_coin_links)
        counter += 1
        # Условие выхода из цикла
        if page >= last_page:
            break
        else:
            page += 1

    # for link in all_coin_links:
    #     html = get_html(link)
    #     data = get_page_data(html)
    #     write_csv(data)
    
    end = datetime.now()
    total = end - start
    print('TOTAL TIME=>', str(total))

if __name__ == '__main__':
    main()