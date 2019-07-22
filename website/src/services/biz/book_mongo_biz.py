#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          book_mongo_biz.py
@Version:       
@Time:          2019-06-11 14:18
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-11 14:18
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from crawler.entities.book import Book
from crawler.services.biz.base_mong_biz import BaseMongoBiz
from crawler.services.biz.base_mongo_da import BaseMongoDA


class BookMongoBiz(BaseMongoBiz):
	_db = 'DoubanBookApi'
	_col = 'sl_book_info'

	# @classmethod
	# def find_all(cls, filter={}, sort=None, skip=None, limit=None):

	@classmethod
	def find(cls, filter={}, sort=None, skip=None, limit=None):
		result = []

		doc_list = BaseMongoDA.find(cls._db, cls._col, filter, sort, skip, limit)

		if None is not doc_list and len(doc_list) > 0:
			for doc in doc_list:
				obj = Book.dict_to_obj(doc)
				if None is not obj:
					result.append(obj)

		return result
