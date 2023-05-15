from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime
import time
import csv
import re
import os
import dotenv

# Загрузка настроек из файла .env
from dotenv import load_dotenv
load_dotenv()

last_page = 2

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






def get_html(page, url):
    # Создаем объект драйвера
    driver = webdriver.Chrome()

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
                    print('!!!!!!!!!!!!!!!!!!!!!!!=>',p.text, 100*page)
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


def get_all_links(counter, html):
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
    time.sleep(1)
    return response.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        name = soup.find('h1', class_='base-text').text.strip()
        print(name)
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
        writer.writerow( ( data['name'], data['price'] ))
        print( data['name'] )

def write_csv_links(data):
    counter = 1
    with open('coin_price_data.csv', 'a', newline='', encoding='utf-8') as file:
        # fieldnames = ['Name', 'Description', 'Website', 'LinkedIn']
        writer = csv.writer(file)
        # writer.writeheader()
        for i in data:
            writer.writerow( ( i ))
            print( 'SAVE=>', counter, i )
            counter += 1


def main():
    start = datetime.now()
    all_coin_links = []
    page = 1
    # Создаем глобальный счетчик
    counter = 1
    while True:
        # Формируем ссылку на текущую страницу
        url = f'https://coinmarketcap.com/' if page == 1 else f'https://coinmarketcap.com/?page={page}'

        html = get_html(page, url)
        all_coin_links = get_all_links(counter, html)
        # write_csv_links(all_coin_links)
        # print('PAGE=>', page, all_coin_links)

        
        # Условие выхода из цикла
        if page >= last_page:
            break
        else:
            page += 1

    for link in all_coin_links:
        html = get_html_data(link)
        data = get_page_data(html)
        write_csv(data)
    
    end = datetime.now()
    total = end - start
    print('TOTAL TIME=>', str(total))

if __name__ == '__main__':
    main()