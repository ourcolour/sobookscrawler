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

from crawler.services.baidu_yun_service import BaiduYunService
from crawler.services.sobooks_crawler_service import SobooksCrawlerService


def main():
	with BaiduYunService() as svs:
		svs.save_to_yun()
	return
	SobooksCrawlerService.new_range_tasks(1, 15)


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
