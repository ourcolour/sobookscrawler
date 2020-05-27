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

from entities.book_model import BookModel

from services.biz.bases.base_mongo_biz import BaseMongoBiz


class BookMongoBiz(BaseMongoBiz[BookModel]):
	pass

# _db = 'DoubanBookApi'
# _col = 'sl_book_info'
#
# @classmethod
# def find_one(cls, criteria={}, sort=None):
# 	doc = BookModel.objects(__raw__=criteria)
# 	if sort:
# 		doc = doc.order_by(sort)
# 	doc = doc.first()
# 	return doc
#
# @classmethod
# def find(cls, criteria={}, sort=None, skip=None, limit=None):
# 	result = []
#
# 	# doc_list = BaseMongoDA.find(cls._db, cls._col, filter, sort, skip, limit)
# 	doc_list = BookModel.objects(__raw__=criteria)
# 	if sort:
# 		doc_list = doc_list.order_by(sort)
# 	if skip:
# 		doc_list = doc_list.skip(skip)
# 	if limit:
# 		doc_list = doc_list.limit(limit)
# 	# BaseMongoDA.find(cls._db, cls._col, filter, sort, skip, limit)
#
# 	if None is not doc_list and len(doc_list) > 0:
# 		for doc in doc_list:
# 			obj = Book.dict_to_obj(doc)
# 			if None is not obj:
# 				result.append(obj)
#
# 	return result
