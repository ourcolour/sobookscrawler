#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_mongo_biz.py.bak
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
from typing import TypeVar, Generic

from bson import ObjectId
from mongoengine.base import TopLevelDocumentMetaclass

from crawler.entities.base_model import BaseModel

# Definations
T = TypeVar('T', BaseModel, None)


# Class
class BaseMongoBiz(Generic[T]):
	@classmethod
	def _get_generic_member_type(cls):
		result = None

		if hasattr(cls, '__orig_bases__'):
			arr = getattr(cls, '__orig_bases__')
			if arr and len(arr) > 0:
				generic_type = arr[0]
				arr = getattr(generic_type, '__args__')
				if arr and len(arr) > 0:
					generic_type = arr[0]
					if isinstance(generic_type, TopLevelDocumentMetaclass):
						result = generic_type
					else:
						print(generic_type)
						print(type(generic_type))

		if None is result:
			raise ValueError('Invalid generic member `T` in BaseMongoBiz.')

		return result

	@classmethod
	def check_args(cls, model):
		if None is model:
			raise ValueError('Invalid argument(s) `model`.')

	@classmethod
	def add(cls, model) -> T:
		cls.check_args(model)

		# Set `inTime` field with current time
		model.inTime = datetime.now().utcnow()
		# Do insert
		model.save()

		return model

	@classmethod
	def update(cls, object_id, new_model) -> T:
		cls.check_args(new_model)

		# Find
		if isinstance(object_id, str):
			object_id = ObjectId(object_id)
		old_model = cls._get_generic_member_type().objects(__raw__={'_id': object_id}).first()

		return cls.update_by_entity(old_model, new_model)

	@classmethod
	def update_by_entity(cls, old_model, new_model) -> T:
		cls.check_args(old_model)
		cls.check_args(new_model)

		# Set `id` field with old entity's id
		new_model.id = old_model.id
		# Set `inTime` field with old entity's time
		new_model.inTime = old_model.inTime
		# Set `editTime` field with current time
		new_model.editTime = datetime.now().utcnow()
		# Do update
		new_model = new_model.save()

		return new_model

	@classmethod
	def count(cls, criteria=dict()) -> int:
		total_count = cls._get_generic_member_type().objects(__raw__=criteria).count()
		return total_count

	@classmethod
	def find_one(cls, criteria={}, sort=None):
		query = cls._get_generic_member_type().objects(__raw__=criteria)
		if sort:
			query = query.order_by(sort)

		model = query.first()
		return model

	@classmethod
	def find(cls, criteria={}, sort=None, skip=None, limit=None):
		query = cls._get_generic_member_type().objects(__raw__=criteria)
		if sort:
			query = query.order_by(*sort)
		if skip:
			query = query.skip(skip)
		if limit:
			query = query.limit(limit)
		return query
