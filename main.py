#!/usr/bin/python
#*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from random import choice
import csv
import time
import random

# url = "https://banlanyinxiang.1688.com/page/offerlist.htm"

def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_data_price(href):
    data = get_html(href)
    soup = BeautifulSoup(data, 'lxml')
    return soup

def write_csv(data, nfile='noname'):
    with open(nfile+'.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)

def ip(ips):
    l = []
    for ip in ips.split(','):
        l.append(ip.strip())

    return choice(l)            


def get_page_html(html, nfile):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('ul', class_='offer-list-row').find_all('li', class_='offer-list-row-offer')
    time = 1


    for ad in ads:
        print(str(time)+" товар")
        price_add = []

        try:
          image_href = ad.find('div', class_='image').find('a').get('href')
          data_image = get_data_price(image_href)
          image = data_image.find('a', class_='box-img').find('img').get('src')
          price_add.append(image)


        except:
          image = "nothing"
          price_add.append(image)

        try:
            title = ad.find('div', class_='title-new').find('a').text
            price_add.append(title)


        except:
            title = "None"
            price_add.append(title)

        try:
            d = {'amount': 'amount','price': 'price', }
            price_href = ad.find('div', class_='image').find('a').get('href')
            data_price = get_data_price(price_href)

            for key, value in d.items():
                # r = random.randint(2, 9) / 2.5
                data_price_table = data_price.find('div', class_='d-content').find('tr', class_=value).find_all('td')
                for price in data_price_table:
                    try:
                        price_ad = price.find('span', class_='value').text
                        price_add.append(price_ad)
                    except:
                        price_ad = "none"

        except:
            price_href = "None"
        time+=1
        write_csv(price_add, nfile)



def main():

    # url = "https://hedao3d.1688.com/page/offerlist.htm?"
    useragents  = ''
    proxys      = ''
    file        = input("Введите название файла: ")
    useragent   = input("Введите юзерагент: ")
    proxy       = input("Введите от 2-х до 100 прокси ip адрес формата 52.91.226.223:3128: ")
    useragents  = useragent
    proxys      = proxy

    useragent_s = {'User-Agent': ip(useragents)}
    proxy_s     = {'http': 'http://' + ip(proxys)}

    print(useragent_s)
    print(proxy_s)


    url = input("Введите url формата 'https://hedao3d.1688.com/page/offerlist.html': ")
    page_input = input("Введите число страниц в магазине: ")
    page = "?&pageNum="
    total_page = int(page_input)
    # proxys = open('proxy.txt').read().split('\n')

    for i in range(0, total_page):
        r = random.randint(2, 9) / 2.5

        try:
        #     if i >= 3 or i >=6 or i >= 9 or i>= 12:
        #         print("Задержка на" + str(r))
        #         time.sleep(r)

            print("Начинаем парсить: ")
            count = 0
            url_gen = url+page+str(i)
            get_html2 = get_html(url_gen, useragent_s, proxy_s)
            get_page_html(get_html2, file)
            time.sleep(r)
            pg = i+1
            print("Закончили " + str(pg) + " стр.")


        except:
            print("Что-то пошло не так, повторите запуск")
            input()



if __name__ == '__main__':
    main()
    input()