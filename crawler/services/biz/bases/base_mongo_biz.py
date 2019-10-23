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
			if arr:
				generic_type = arr[0]
				arr = getattr(generic_type, '__args__')
				if arr:
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

	# @classmethod
	# def update(cls, object_id, new_model) -> T:
	# 	cls.check_args(new_model)
	#
	# 	# Find
	# 	if isinstance(object_id, str):
	# 		object_id = ObjectId(object_id)
	# 	old_model = cls._get_generic_member_type().objects(__raw__={'_id': object_id}).update(unset__author)
	#
	# 	return cls.update_by_model(old_model, new_model)



	@classmethod
	def update_by_objectid(cls, object_id, new_model) -> T:
		cls.check_args(new_model)

		# Find
		if isinstance(object_id, str):
			object_id = ObjectId(object_id)
		old_model = cls._get_generic_member_type().objects(__raw__={'_id': object_id}).first()

		return cls.update_by_model(old_model, new_model)

	@classmethod
	def update_by_model(cls, old_model, new_model) -> T:
		cls.check_args(old_model)
		cls.check_args(new_model)

		# Set `id` field with old entity's id
		# new_model.id = old_model.id
		# Set `inTime` field with old entity's time
		# new_model.inTime = old_model.inTime
		# Set `editTime` field with current time
		# new_model.editTime = datetime.now().utcnow()
		# Do update
		# new_model = new_model.save()

		# Convert properties of new_model into dict type
		new_model_properties_dict = new_model.to_mongo().to_dict()

		# Update old_model's properties with new values
		for (k, v) in new_model_properties_dict.items():
			# Ignore '_id' field
			if '_id' == k:
				continue
			# Assign value
			old_model[k] = v
			# print('KV: {} = {}'.format(k, v))
			pass

		# Set `editTime` field with current time
		old_model.editTime = datetime.now().utcnow()
		# Do update
		old_model = old_model.save()

		return old_model

	@classmethod
	def count(cls, criteria=None) -> int:
		if None is criteria:
			criteria = dict()

		total_count = cls._get_generic_member_type().objects(__raw__=criteria).count()
		return total_count

	@classmethod
	def find_one(cls, criteria=None, sort=None):
		if None is criteria:
			criteria = dict()

		query = cls._get_generic_member_type().objects(__raw__=criteria)
		if sort:
			query = query.order_by(sort)

		model = query.first()
		return model

	@classmethod
	def find(cls, criteria=None, sort=None, skip=None, limit=None):
		if None is criteria:
			criteria = dict()

		query = cls._get_generic_member_type().objects(__raw__=criteria)
		if sort:
			query = query.order_by(*sort)
		if skip:
			query = query.skip(skip)
		if limit:
			query = query.limit(limit)
		return query

	@classmethod
	def delete(cls, criteria=None) -> int:
		if None is criteria:
			criteria = dict()

		query = cls._get_generic_member_type().objects(__raw__=criteria)

		affected_rows = query.delete()
		# affected_rows = 0#query.delete()

		return affected_rows

	@classmethod
	def delete_by_entity(cls, model) -> int:
		if not model:
			return 0

		criteria = {'_id': model._id}
		affected_rows = cls.delete(criteria=criteria)

		return affected_rows
