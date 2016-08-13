# encoding=utf-8
# Created by -==donglida==- on 16-7-27 下午3:40
# 试验一下中文的输入情况如何呢？是不是使用了新的字体会更漂亮一些？看来只能是使用OpenJDK的Java环境了，用
# Orcale Java SDK会无法显示出Ubuntu16.04的新加装默认字体

from pyquery import PyQuery as pq
import requests
import os
import json


class BookList:
    base_url = 'http://readfree.me'
    list_url = 'http://readfree.me/?page={0}'
    book_url = 'http://readfree.me/book/{0}/'
    login_url = 'http://readfree.me/accounts/signin'
    headers = {
        'Host': 'readfree.me',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://readfree.me/accounts/signin/',
        'Connection': 'keep-alive'
    }

    session = requests.session()

    def __init__(self):
        self.login_data = {
            'email': os.getenv('EMAIL'),
            'password': os.getenv('PASSWORD')
        }
        if self.login_in():
            self.doc = pq(url=self.base_url)
            self.total_page_num = int(self.doc('.container')('.hidden-phone:last').text())
        else:
            print('Error in login')

    def get_page(self, page_number):
        self.doc = pq(url=self.list_url.format(page_number))

    def process_detail(self, content, detail):
        # 简介
        detail['summary'] = content('.book-summary')('pre').text()
        # Tags，一般情况下为4个
        tag_count = len(content('#book-tags')('li'))
        tag_info = {}
        for i in range(0, tag_count):
            tag_info.update({content('#book-tags')('li').eq(i).text():
                                 content('#book-tags')('li').eq(i)('a').attr('href')})
        detail['tag_info'] = tag_info
        # 类似书箱，保存了书名和id号
        similar_count = len(content('#similar-books')('li'))
        similar_info = {}
        for i in range(0, similar_count):
            similar_info.update({
                content('#similar-books')('li').eq(i)('img').attr('title'):
                    content('#similar-books')('li').eq(i)('a').attr('href').split('/')[-2]})
        detail['similar_info'] = similar_info
        # 下载的地址
        # 下载次数，对应的是某几个版本
        down_nums = [int(x.text()) for x in content('.book-down')('span').items()]
        # 收藏次数，对应的是某几个版本
        wish_nums = [int(x.text()) for x in content('.book-wish')('span').items()]
        # 推送次数，对应的是某几个版本
        push_nums = [int(x.text()) for x in content('.push-num').items()]
        # 不同版本的下载地址及标题
        versions_info = [{self.base_url + x.attr('href'), x.attr('title')} for x in content('a.book-down').items()]
        # 版本数目
        version_num = int(''.join(x for x in content('h4').text() if x.isdigit()))
        versions_info = {}
        for i in range(0, version_num):
            versions_info.update({'versions':i, 'down_url':})
            detail['editions']
        # 同一书籍的不同版本及同一版本下的各种评论

        return detail

    def process_single_page(self):
        book_count = len(self.doc('.container')('.pjax'))
        book_list = []
        for i in range(0, book_count, 2):
            # 0-封面图片地址 1-书名、详情地址、ID号
            cover_img_url = self.doc('.container')('.pjax').eq(i)('.book-cover.img-rounded').attr('src')
            book_info = {'book_cover_img_url': cover_img_url if cover_img_url.__contains__(
                'http') else self.base_url + cover_img_url,
                         'name': self.doc('.container')('.pjax').eq(i + 1).text(),
                         'id': self.doc('.container')('.pjax').eq(i + 1).attr('href').split('/')[-2]}
            book = self.session.get(self.book_url.format(book_info['id']), headers=self.headers)
            book_content = book.content.decode('utf-8')
            book_info = self.process_detail(pq(book_content), book_info)
            book_list.append(book_info)
        return book_list

    def login_in(self):
        res = self.session.post(self.login_url, self.login_data, headers=self.headers)
        self.login_data['csrfmiddlewaretoken'] = res.cookies['csrftoken']
        res = self.session.post(self.login_url, data=self.login_data, headers=self.headers)
        return True if res.status_code == 200 else False

    def process_single_book(self, id):
        pass


booklist = BookList()
first_page = booklist.process_single_page()
from pprint import pprint
pprint(json.dumps(first_page, ensure_ascii=False, indent=2))
