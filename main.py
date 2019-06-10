#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          main.py
@Version:       
@Time:          2019/5/22 11:35
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/22 11:35
2.  TO-DO
+-------------------------------------------------
'''
from crawler.services.douban_book_service import DoubanBookService

__author__ = 'cc'

from datetime import datetime

from crawler.services.baidu_yun_service import BaiduYunService


def test_user_agent():
	from fake_useragent import UserAgent
	ua = UserAgent()

	for i in range(1, 100):
		print('{} - {}'.format(i, ua.random))

	return


def main():
	# Fatch newer
	# SobooksCrawlerExecutor.new_range_tasks(1, 1)

	# Download newer
	with BaiduYunService() as svs:
		netdisk_folder_name = '08_book_newincome'
		from_date = datetime.strptime('2019-05-01', '%Y-%m-%d')
		to_date = datetime.strptime('2019-05-5', '%Y-%m-%d')

		download_task_list = svs.query_tasks(
			filter={'$and': [
				{'publishTime': {'$gte': from_date}},
				# {'publishTime': {'$lte': to_date}},
			]},
			sort=[
				('publishTime', -1),
				('inTime', 1),
			],
		)

		for idx, t in enumerate(download_task_list):
			print('{:>3d}# 《{}》 {}'.format(idx + 1, t.title, t.baiduUrl))

		svs.save_many(download_task_list, netdisk_folder_name=netdisk_folder_name)


# SobooksCrawlerService.new_range_tasks(1, 15)


def _code_generator():
	a = '''
		@property
		def <<>>(self):
			return self._<<>>
	
		@<<>>.setter
		def <<>>(self, value):
			self._<<>> = value
	'''

	lst = [
		'alt',
		'alt_title',
		'author',
		'author_intro',
		'binding',
		'catalog',
		'cips',
		'image',
		'images',
		'isbn10',
		'isbn13',
		'origin_title',
		'pages',
		'price',
		'pubdate',
		'publisher',
		'rating',
		'subtitle',
		'summary',
		'tags',
		'title',
		'translator',
		'url',
	]

	for l in lst:
		print(a.replace('<<>>', l, -1))
		print('')


if __name__ == '__main__':
	# main()
	# _code_generator()

	book_id_list = [
		'26361453',
		'27009452',
		'24695948',
		'27155214',
		'26639302',
		'26289557',
		'26882520',
		'26581246',
		'25879618',
		'25844726',
		'27147066',
		'27092579',
		'27056210',
		'30121217',
		'27084077',
		'26959626',
		'27603904',
		'27101663',
		'27115938',
		'27593864',
		'25883310',
		'27086018',
		'27124847',
		'27605896',
		'3673771',
		'27036522',
		'27199957',
		'26939261',
		'26939269',
		'27197943',
		'27157960',
		'28531867',
		'27106877',
		'27117054',
		'27667777',
		'27060598',
		'27046333',
		'27616950',
		'25879507',
		'26666408',
		'26426959',
		'26816981',
		'26902009',
		'26921196',
	]

	with DoubanBookService() as svs:
		for book_id in book_id_list:
			svs.get_book(book_id)
