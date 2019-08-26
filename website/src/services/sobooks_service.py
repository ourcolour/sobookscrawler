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

from entities.sobooks_model import SobooksModel

DEFAULT_PAGE_SIZE = 10


class SobooksService(object):

	def find_by_isbn(self, isbn):
		return SobooksModel.objects(__raw__={'isbn': isbn})

	def find(self, filter={}, page_no=1, page_size=DEFAULT_PAGE_SIZE):
		return SobooksModel.objects(__raw__=filter) \
			.order_by('+inTime') \
			.paginate(page=page_no, per_page=page_size)