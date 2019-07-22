#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_mong_biz.py.bak
@Version:       
@Time:          2019-06-11 14:13
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-11 14:13
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from datetime import datetime

from crawler.services.biz.base_mongo_da import BaseMongoDA


class BaseMongoBiz(object):
	_db = None
	_col = None

	@classmethod
	def check_args(cls, entity):
		if None is entity:
			raise ValueError('Invalid argument(s).')

	@classmethod
	def add(cls, entity):
		cls.check_args(entity)

		# Set `inTime` field with current time
		entity.inTime = datetime.now()

		doc = entity.obj_to_dict()
		entity.id = BaseMongoDA.add(cls._db, cls._col, doc)
		return entity

	@classmethod
	def update_by_entity(cls, old_entity, new_entity):
		cls.check_args(old_entity)
		cls.check_args(new_entity)

		# Set `id` field with old entity's id
		new_entity.id = old_entity.id
		# Set `inTime` field with old entity's time
		new_entity.inTime = old_entity.inTime
		# Set `editTime` field with current time
		new_entity.editTime = datetime.now()

		filter = {'_id': old_entity.id}
		doc = new_entity.obj_to_dict()

		affected = BaseMongoDA.replace_one(cls._db, cls._col, filter, doc)

		return new_entity, affected

	@classmethod
	def count(cls, criteria):
		return BaseMongoDA.count(cls._db, cls._col, criteria)

	@classmethod
	def find_one(cls, filter):
		return BaseMongoDA.find_one(cls._db, cls._col, filter)
