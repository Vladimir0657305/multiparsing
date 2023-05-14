import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import time
import csv
import os
import dotenv

# Загрузка настроек из файла .env
from dotenv import load_dotenv
load_dotenv()

last_page = 3

base_url = "https://app.dealroom.co/"
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

page = 1
# Создаем глобальный счетчик
counter = 1

# Сохраняем результаты в CSV-файл
# with open('dealroom_data.csv', 'w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Name', 'Description', 'Website', 'LinkedIn']
# writer = csv.DictWriter(file, fieldnames=fieldnames)
# writer.writeheader()
# for firm_data in firms_data:
#     writer.writerow(firm_data)

def get_html(url):
    # Загружаем страницу
    response = session.get(url)
    # Ожидание загрузки страницы
    time.sleep(10)
    return response.text

def get_all_links(html):
    # Получение HTML-кода страницы с результатами поиска
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', class_='cmc-link')
    print(links)


def main():
    while True:
        # Формируем ссылку на текущую страницу
        url = f'https://coinmarketcap.com/' if page == 1 else f'https://coinmarketcap.com/?page={page}'
        
        all_coin_links = [urljoin(base_url, link['href']) for link in links]


        # Условие выхода из цикла
        if page >= last_page:
            break
        else:
            page += 1

    


if __name__ == '__main__':
    main()