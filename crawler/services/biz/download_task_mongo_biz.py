#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          download_task_mongo_biz.py
@Version:       
@Time:          2019/5/23 13:20
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/23 13:20
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import crawler.configs  as cfg
from crawler.entities.download_task import DownloadTask
from crawler.services.biz.base_mongo_da import BaseMongoDA


class DownloadTaskMongoBiz(object):
	_db = cfg.MONGO_DATABASE
	_col = cfg.MONGO_COLLECTION

	@classmethod
	def _check_args(cls, entity):
		if None is entity:
			raise ValueError('Invalid argument(s).')

	@classmethod
	def add(cls, entity):
		cls._check_args(entity)
		doc = entity.obj_to_dict()
		return BaseMongoDA.add(cls._db, cls._col, doc)

	@classmethod
	def update_by_id(cls, object_id, entity):
		cls._check_args(entity)

		filter = {'_id': object_id}
		doc = entity.obj_to_dict()

		return BaseMongoDA.replace_one(cls._db, cls._col, filter, doc)

	@classmethod
	def count(cls, criteria):
		return BaseMongoDA.count(cls._db, cls._col, criteria)

	@classmethod
	def find_by_url(cls, entity):
		baiduUrl = entity.baiduUrl
		ctUrl = entity.ctUrl

		sub_criteria = []
		if None is not baiduUrl and len(baiduUrl) > 0:
			sub_criteria.append({'baiduUrl': baiduUrl})
		if None is not ctUrl and len(ctUrl) > 0:
			sub_criteria.append({'ctUrl': ctUrl})

		criteria = {'$or': sub_criteria}

		doc = BaseMongoDA.find_one(cls._db, cls._col, criteria)
		if None is not doc:
			doc = DownloadTask.dict_to_obj(doc)

		return doc

	@classmethod
	def find_one(cls, filter):
		return BaseMongoDA.find_one(cls._db, cls._col, filter)

	@classmethod
	def find(cls, filter={}, sort=None, skip=None, limit=None):
		result = []

		doc_list = BaseMongoDA.find(cls._db, cls._col, filter, sort, skip, limit)

		if None is not doc_list and len(doc_list) > 0:
			for doc in doc_list:
				obj = DownloadTask.dict_to_obj(doc)
				if None is not obj:
					result.append(obj)

		return result
