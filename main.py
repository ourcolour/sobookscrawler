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


def main():
	netdisk_folder_name = '08_book_newincome'
	from_date = datetime.strptime('2019-05-4', '%Y-%m-%d')
	to_date = datetime.strptime('2019-05-25', '%Y-%m-%d')
	filter = {'$and': [
		{'publishTime': {'$gte': from_date}},
		{'publishTime': {'$lte': to_date}},
	]}

	with BaiduYunService() as svs:
		download_task_list = svs.query_tasks(filter=filter)
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
