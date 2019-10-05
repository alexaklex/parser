#!/usr/bin/python
#*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from random import choice
import csv
import time
import random
import os
import openpyxl
from PIL import Image
import glob
import re
from datetime import datetime

# url = "https://banlanyinxiang.1688.com/page/offerlist.htm"


def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text



def get_data_price(href):
    data = get_html(href)
    soup = BeautifulSoup(data, 'lxml')
    return soup

def get_img(image, name="imgfolder"):
    print(image)
    for i in image:
        urls = i.split('/')[-1].split('.')[0]
        # print(urls)
        response = requests.get(i)
        if response.status_code == 200:
            with open(os.path.abspath(name+"/"+datetime.now().strftime('%H%M%S')+".jpg"), 'wb') as f:
                time.sleep(1)
                f.write(response.content)


def edit_excel(excel, path="fold", count=1):
    img_m = []
    xfile = openpyxl.load_workbook(excel)
    sheet_ranges = xfile['Worksheet']
    sheet_ranges.column_dimensions['A'].width = 30
    for i in range(1, int(count)+1):
        sheet_ranges.row_dimensions[i].height = 70
        png_loc1 = os.path.abspath(str(path)+"/" + str(i) + ".jpg")
        ws = xfile.active
        img = openpyxl.drawing.image.Image(png_loc1)
        img_m.append(img)
        img.anchor(ws.cell('A' + str(i)))


    for i in img_m:
        ws.add_image(i)
        xfile.save(excel)



def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    resized_image.save(output_image_path)


def write_csv(data, nfile='noname'):
    with open(nfile+'.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data)

def ip(ips):
    l = []
    for ip in ips.split(','):
        l.append(ip.strip())

    return choice(l)            


def get_page_html(html, nfile, name_img=None):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('ul', class_='offer-list-row').find_all('li', class_='offer-list-row-offer')
    time = 1
    all_image = []

    for ad in ads:
        print(str(time)+" товар")
        price_add = ['img']


        try:
          image_href = ad.find('div', class_='image').find('a').get('href')
          data_image = get_data_price(image_href)
          #Получили ссылку на img
          image = data_image.find('a', class_='box-img').find('img').get('src')
          price_add.append(image)
          all_image.append(image)
        except:
          image = "None"
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
                        price_ad = "None"

        except:
            price_href = "None"

        time+=1
        write_csv(price_add, nfile)
    # Скачиваем картинки
    get_img(all_image, name_img)
    print(len(all_image))


def main():
    xls_m = []
    img_resize = []
    path_main = os.path.abspath("")
    xls = glob.glob(path_main+"/*.xlsx")
    if len(xls) > 0:
        [xls_m.append(i) for i in xls]


        for i in xls_m:
            formar = i.split('/')
            xls_f = formar[-1].split(".")[1]
            if xls_f == 'xlsx' or xls_f == 'xls' or xls_f  =='xlsm' or xls_f == 'xltm':
                print("У Вас есть файлы excel  "+"'"+xls_f+"'")
                name_xls = input("Введите название файла xls: ")
                count = input("Введите количество строк в файле: ")
                name_folder = input("Введите название папки img который вы хотет записать в файл: ")
                folds = os.path.abspath(name_folder)
                img = os.listdir(folds)
                if not os.path.exists(folds+'_resize'):
                    os.makedirs(os.path.abspath(folds+'_resize'))
                else:
                    print("Такая папка уже есть")

                if len(img) > 0:
                    [img_resize.append(i) for i in img]


                for num,i in enumerate(sorted(img_resize)):
                    num+=1
                    numb = str(num)+".jpg"
                    resize_image(input_image_path=folds+'/'+i, output_image_path=folds+'_resize'+'/'+numb, size=(70, 70))
                edit_excel(name_xls, folds+'_resize', count)
        exit()

    folder = input("Введите название папки для картинок: ")
    if not os.path.exists(folder):
        os.makedirs(os.path.abspath(folder))
    else:
        print("Такая папка уже есть")

    # url = "https://hedao3d.1688.com/page/offerlist.htm?"
    useragents = ''
    proxys = ''
    file = input("Введите название файла: ")
    useragent = input("Введите юзерагент: ")
    proxy = input("Введите от 2-х до 100 прокси ip адрес формата 52.91.226.223:3128: ")
    useragents = useragent
    proxys = proxy

    useragent_s = {'User-Agent': ip(useragents)}
    proxy_s = {'http': 'http://' + ip(proxys)}

    print(useragent_s)
    print(proxy_s)


    url = input("Введите url формата 'https://hedao3d.1688.com/page/offerlist.html': ")
    page_input = input("Введите число страниц в магазине: ")
    page = "?&pageNum="
    total_page = int(page_input)
    # proxys = open('proxy.txt').read().split('\n')
    total_page+=1
    for i in range(1, total_page):
        r = random.randint(2, 9) / 2.5

        try:
        #     if i >= 3 or i >=6 or i >= 9 or i>= 12:
        #         print("Задержка на" + str(r))
        #         time.sleep(r)

            print("Начинаем парсить: ")
            count = 0
            url_gen = url+page+str(i)
            get_html2 = get_html(url_gen, useragent_s, proxy_s)
            get_page_html(get_html2, file, folder)
            time.sleep(r)
            print("Закончили " + str(i) + " стр.")


        except:
            print("Что-то пошло не так, повторите запуск")
            input()



if __name__ == '__main__':
    main()
    input()