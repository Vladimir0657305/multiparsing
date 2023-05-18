from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import requests
from multiprocessing import Pool
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
# import re
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

def get_html(page, url):

    options = Options()
    options.add_argument('--headless')

    # Создаем объект драйвера
    driver = webdriver.Chrome(options=options)

    # Загружаем страницу
    driver.get(url)

    while True:
        # Получение HTML-кода страницы фирмы
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tab = soup.select_one('table')
        tds = tab.find_all('td')
        for td in tds:
            try:
                p = td.find('p', class_='sc-4984dd93-0 ihZPK')
                if p.text == str(100 * page):
                    print('!!!!!!!!!!!!!!!!!!!!!!!=>', p.text, 100*page)
                    # Получаем HTML-код таблицы
                    html = driver.page_source
                    # Закрываем драйвер
                    driver.quit()
                    return html
            except:
                pass

        # Если не нашли нужный элемент, прокручиваем страницу
        driver.execute_script("window.scrollBy(0, 4000);")
        time.sleep(1)


def get_all_links(html):
    links_all = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='sc-beb003d5-3')
    if table is not None:
        trs = table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) >= 4:
                td = tds[2]
                link = td.find('a', class_='cmc-link')
                if link is not None:
                    href = link.get('href')
                    links_all.append(urljoin(base_url, href))
    return links_all

def get_html_data(url):
    response = requests.get(url)
    time.sleep(2)
    return response.text

def get_page_data(url):
    response = requests.get(url)
    # response = session.get(url)
    time.sleep(1)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = 'None'
    price = 'None'
    try:
        name_label = soup.find('h1', class_='sc-8755d3ba-0 kGceQv base-text')
        if name_label:
            name = name_label.find(
                'span', class_='sc-8755d3ba-0 frXndb').text.strip()

    except:
        name = None
    try:
        price_div = soup.find(
            'div', class_='sc-8755d3ba-0 fiIhCU flexStart alignBaseline')
        price = price_div.find(
            'span', class_='sc-8755d3ba-0 PaOrf base-text').text.strip()
        if (price == None):
            print(soup)
    except:
        pass
    print('NAME PRICE=>', name, price)
    data = {'name': name, 'price': price}
    return data

# Сохраняем результаты в CSV-файл
def write_csv(data):
    with open('coin_price_data.csv', 'a', newline='', encoding='utf-8') as file:
        # fieldnames = ['Name', 'Price']
        writer = csv.writer(file)
        # writer.writeheader()
        writer.writerow((data['name'], data['price']))

def write_csv_links(data):
    with open('coin_price_links.csv', 'a', newline='', encoding='utf-8') as file:
        # fieldnames = ['Name', 'Price']
        writer = csv.writer(file)
        # writer.writeheader()
        for i in data:
            writer.writerow([i])

def make_all(link):
    data = get_page_data(link)
    print('LINK=>',  link)
    while data['name'] == 'None':
        print('RE-DOWNLOAD', data['name'], data['price'], link)
        time.sleep(1)
        data = get_page_data(link)
    if (data['name'] != 'None'):
        print('DDDAAATTTTAAAA', data['name'], data['price'])
        write_csv(data)

def main():
    start = datetime.now()
    all_coin_links = []
    all_coin_links_to_scrape = []
    page = 1
    
    # В цикле while формируем список ссылок для парсинга
    while True:
        # Формируем ссылку на текущую страницу
        url = f'https://coinmarketcap.com/' if page == 1 else f'https://coinmarketcap.com/?page={page}'

        html = get_html(page, url)
        all_coin_links = get_all_links(html)
        write_csv_links(all_coin_links)
        all_coin_links_to_scrape.extend(all_coin_links)

        # Условие выхода из цикла
        if page >= last_page:
            break
        else:
            page += 1

    with Pool(10) as p:
        p.map(make_all, all_coin_links_to_scrape)

    end = datetime.now()
    total = end - start
    print('TOTAL TIME=>', str(total))

if __name__ == '__main__':
    main()
