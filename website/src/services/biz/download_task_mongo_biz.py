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

from crawler.entities.download_task import DownloadTask
from crawler.services.biz.bases.base_mongo_biz import BaseMongoBiz
from crawler.services.biz.bases.base_mongo_da import BaseMongoDA


class DownloadTaskMongoBiz(BaseMongoBiz):
	_db = 'DoubanBookApi'
	_col = 'cloud_storage'

	@classmethod
	def find_by_url(cls, entity):
		baiduUrl = entity.baiduUrl
		ctUrl = entity.ctUrl

		sub_criteria = list()
		if None is not baiduUrl and baiduUrl:
			sub_criteria.append({'baiduUrl': baiduUrl})
		if None is not ctUrl and ctUrl:
			sub_criteria.append({'ctUrl': ctUrl})

		criteria = {'$or': sub_criteria}

		doc = BaseMongoDA.find_one(cls._db, cls._col, criteria)
		if None is not doc:
			doc = DownloadTask.dict_to_obj(doc)

		return doc

	@classmethod
	def find(cls, criteria=None, sort=None, skip=None, limit=None):
		if None is criteria:
			criteria = dict()

		result = []

		doc_list = BaseMongoDA.find(cls._db, cls._col, criteria, sort, skip, limit)

		if None is not doc_list and doc_list:
			for doc in doc_list:
				obj = DownloadTask.dict_to_obj(doc)
				if None is not obj:
					result.append(obj)

		return result
