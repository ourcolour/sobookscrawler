#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          sobooks_service.py
@Version:       
@Time:          2019-06-26 17:02
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-26 17:02
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from entities.book_model import BookModel

DEFAULT_PAGE_SIZE = 10


class BookService(object):

	def find_by_isbn(self, isbn):
		return BookModel.objects(__raw__={'isbn13': str(isbn)})

	def find(self, criteria=None, page_no=1, page_size=DEFAULT_PAGE_SIZE):
		if None is criteria:
			criteria = dict()

		return BookModel.objects(__raw__=criteria) \
			.order_by('+inTime') \
			.paginate(page=page_no, per_page=page_size)
