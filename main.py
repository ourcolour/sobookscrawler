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


if __name__ == '__main__':
	main()


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
		'title',
		'author',
		'baiduUrl',
		'ctUrl',
		'createTime',
		'inTime',
		'isbn',
		'secret',
		'formats',
		'tags',
	]

	for l in lst:
		print(a.replace('<<>>', l, -1))
		print('')
