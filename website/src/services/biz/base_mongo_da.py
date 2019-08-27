#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_mongo_da.py
@Version:       
@Time:          2019/5/23 10:22
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/23 10:22
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import pymongo as mgo

import crawler.configs as cfg

DEFAULT_MONGO_HOST = 'localhost'
DEFAULT_MONGO_PORT = 27017


class BaseMongoDA:

	@classmethod
	def __connect__(cls, host=cfg.MONGO_HOST, port=cfg.MONGO_PORT):
		if None is host or not host:
			host = DEFAULT_MONGO_HOST
		if None is port or port < 1 or port > 65535:
			port = DEFAULT_MONGO_PORT

		conn = mgo.MongoClient(host=host, port=port)

		return conn

	@classmethod
	def add(cls, db, col, doc):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')
		if None is doc:
			raise ValueError('Invalid document value.')

		result = None

		with cls.__connect__() as conn:
			col = conn.get_database(db).get_collection(col)
			result = col.insert(doc)

		return result

	@classmethod
	def __remove__(cls, db, col, criteria):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')
		pass

	@classmethod
	def __update__(cls, db, col, criteria, doc):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')
		if None is doc:
			raise ValueError('Invalid document value.')

	@classmethod
	def replace_one(cls, db, col, filter, doc, upsert=False):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')
		if None is doc:
			raise ValueError('Invalid document value.')

		result = None

		with cls.__connect__() as conn:
			col = conn.get_database(db).get_collection(col)
			result = col.replace_one(filter, doc, upsert)

		return result

	@classmethod
	def __remove__(cls, db, col, filter, collation=None):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')

		result = None

		with cls.__connect__() as conn:
			col = conn.get_database(db).get_collection(col)
			result = col.delete_one(filter, collation)

		return result

	@classmethod
	def find(cls, db, col, criteria={}, sort=None, skip=None, limit=None):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')
		if None is criteria:
			criteria = dict()

		result = []

		with cls.__connect__() as conn:
			col = conn.get_database(db).get_collection(col)
			# if None is not filter:
			# 	cursor = col.find(filter)
			# else:
			# 	cursor = col.find()
			with col.find(criteria) as cursor:
				if None is not sort:
					if isinstance(sort, tuple):
						sort = [sort]
					cursor = cursor.sort(sort)
				if None is not skip:
					cursor = cursor.skip(skip)
				if None is not limit:
					cursor = cursor.limit(limit)
				for doc in cursor:
					result.append(doc)

		return result

	@classmethod
	def find_one(cls, db, col, filter=None):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')

		result = None

		with cls.__connect__() as conn:
			col = conn.get_database(db).get_collection(col)
			if None is not filter:
				result = col.find_one(filter)
			else:
				result = col.find_one()

		return result

	@classmethod
	def count(cls, db, col, filter=None):
		if None is db:
			raise ValueError('Invalid database value.')
		if None is col:
			raise ValueError('Invalid collection value.')

		result = None

		with cls.__connect__() as conn:
			col = conn.get_database(db).get_collection(col)
			if None is not filter:
				result = col.count(filter)
			else:
				result = col.count()

		return result
