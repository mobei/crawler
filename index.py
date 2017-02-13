#!/usr/bin/env python
# encoding: utf-8

import time
import random
import os
import requests
from bs4 import BeautifulSoup


HEADERS = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
]

# ====豆瓣读书爬虫练习 未分页===
def books_spider():
    tags = ['心理学', '中国历史', '科普']
    base_url = 'http://www.douban.com/tag/%s/book';
    file_name = 'books.txt'
    content_start_line = '======%s======\n\n'
    content = ''

    for tag in tags:
        url = base_url % tag
        content += content_start_line % tag
        source = requests.get(url, headers=random.choice(HEADERS))
        soup = BeautifulSoup(source.text, 'html.parser')
        books = soup.select('.book-list > dl > dd')
        content += get_books_content(books)

    write_file(file_name, content)

def get_books_content(books):
    content = ''
    file_name = 'books.txt'

    for book in books:
        book_desc = book.find('div', class_="desc").string.strip().split('/')
        book_name = '书名：' + book.find('a', class_="title").string.strip() + '\n'
        book_author = '作者/译者：' + '/'.join(book_desc[0:-3]) + '\n'
        book_public = '出版社：' + '/'.join(book_desc[-3:-2]) + '\n'
        book_price = '价格：' + book_desc[-1] + '\n'
        content += book_name + book_author + book_public + book_price + '\n'
        content += '--------------\n\n'
    
    return content
# ================

# =====相册爬虫练习====

def photos_spider(max_page, step=18):
    targets = {'zh': {'id': '128181217', 'path': '/zhihu/'}, 'zj': {'id': '1613893843', 'path': '/zjl/'}}
    target = targets.get('zh') #知乎回答...
    # target = targets.get('zj') #震惊了...
    
    base_url = 'https://www.douban.com/photos/album/' + target.get('id') + '/?start=%d'    #知乎回答
    file_path = './photos' + target.get('path')

    max_photos = (max_page - 1) * step
    photos_start = range(0, max_photos, step)
    img_els = []

    if not os.path.exists(file_path):
       os.makedirs(file_path)

    if not len(photos_start):
        photos_start = [0]

    for start in photos_start:
        url = base_url % start
        source = requests.get(url, headers=random.choice(HEADERS))
        soup = BeautifulSoup(source.text, 'html.parser')
        img_els.extend(soup.select('.photolst_photo > img'))
    
    for img_el in img_els:
        img_url = img_el.get('src').replace('thumb', 'photo')
        img_name = img_url.split('/')[-1]
        img_source = requests.get(img_url)
        write_file(file_path + img_name, img_source.content, 'wb')

# ================

# ======糗事百科======

def jokes_spider(start_page=1, end_page=2):
    base_url = 'http://www.qiushibaike.com/text/page/%d/'
    pages = range(start_page, end_page)
    content = ''

    for page in pages:
        url = base_url % page
        source = requests.get(url, headers=random.choice(HEADERS))
        soup = BeautifulSoup(source.text, 'html.parser')
        jokes = soup.select('.content-block > .col1 > .article')
        for joke in jokes:
            joke = joke.find('a', class_='contentHerf').find('span')
            strs = ''
            for string in joke.stripped_strings:
                strs += string + '\n'
        
            content += strs + '\n'
            content += '------------\n\n'

    write_file('jokes.txt', content)

# ==================

# ======知乎======

def zhihu_spider():
    base_url = 'https://www.zhihu.com/question/28116784'

    source = requests.get(base_url, headers=random.choice(HEADERS))
    soup = BeautifulSoup(source.text, 'html.parser')
    imgs = soup.select('#zh-question-answer-wrap > .zm-item-answer')

    file_path = './photos/zhihus/'

    if not os.path.exists(file_path):
       os.makedirs(file_path)
    
    for img in imgs:
        img_url = img.find('img')
        # img_name = img_url.split('/')[-1]
        print(img_url)
        # img_source = requests.get(img_url)
        # write_file(file_path+img_name, img_source.content, 'wb')
        

# ==================

# ======util======

def write_file(name, content, wtype='w'):
    with open(name, wtype) as file:
        file.write(content)
        file.close()

# =================

def start():
    print('All started...')
    books_spider()
    # photos_spider(1)
    # jokes_spider(1 ,5)
    # zhihu_spider()
    print('All ended...')

if __name__ == '__main__':
    start()


