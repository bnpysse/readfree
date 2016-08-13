# encoding=utf-8
# Created by -==donglida==- on 16-7-24 下午4:02

import requests
from bs4 import BeautifulSoup
import urllib

login_url = 'http://readfree.me/accounts/signin'
list_url = 'http://readfree.me/'
some_book_url = 'http://readfree.me/book/4720475/'
headers = {
    'Host': 'readfree.me',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://readfree.me/accounts/signin/',
    'Connection': 'keep-alive'
}

get_headers = {
    'Host': 'readfree.me',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://readfree.me/',
    'Connection': 'keep-alive'
}
login_data = {'email': 'bnpysse@aliyun.com',
              'password': 'Gwvbmgfn3631',
              }

session = requests.Session()

res = session.post(login_url, login_data, headers=headers)
login_data['csrfmiddlewaretoken'] = res.cookies['csrftoken']
res = session.post(login_url, data=login_data, headers=headers)
book = session.get(some_book_url, headers=headers)
book_content = book.content.decode('utf-8')
print(book_content)
