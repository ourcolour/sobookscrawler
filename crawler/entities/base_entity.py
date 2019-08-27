#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_entity.py
@Version:       
@Time:          2019-06-06 15:22
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-06 15:22
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import bson
from bson import json_util
import importlib

class BaseEntity(object):
	_id = None
	_inTime = None
	_editTime = None

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		self._id = value

	@property
	def inTime(self):
		return self._inTime

	@inTime.setter
	def inTime(self, value):
		self._inTime = value

	@property
	def editTime(self):
		return self._editTime

	@editTime.setter
	def editTime(self, value):
		self._editTime = value

	def __init__(self):
		pass

	# def __init__(self, title, author, baiduUrl, ctUrl, publishTime, inTime, isbn, secret, formats, tags):
	# 	self._title = title
	# 	self._author = author
	# 	self._baiduUrl = baiduUrl
	# 	self._ctUrl = ctUrl
	# 	self._publishTime = publishTime
	# 	self._inTime = inTime
	# 	self._isbn = isbn
	# 	self._secret = secret
	# 	self._formats = formats
	# 	self._tags = tags

	def obj_to_dict(self, needPropertyNotField=True):
		result = {}

		variables = vars(self).items()
		for k, v in variables:
			if needPropertyNotField and '_id' != k and '_' == k[:1]:
				k = k[1:]
			result[k] = v

		return result

	@classmethod
	def dict_to_obj(cls, dic, module_name=None, class_name=None):
		if None is dic:
			raise ValueError('Invalid argument.')

		# Import module and target class
		if None is module_name or not module_name:
			module_name = cls.__module__
		if None is class_name or not class_name:
			class_name = cls.__name__
		target_module = importlib.import_module(module_name)
		target_class = getattr(target_module, class_name)

		# New instance
		# result = DownloadTask()
		result = target_class()

		for (k, v) in dic.items():
			# if needPropertyNotField and '_' != k[:1]:
			# 	k = "_" + k
			setattr(result, k, v)

		return result

	def to_json(self):
		obj = self.obj_to_dict(self)
		return bson.json_util.dumps(obj)

	@classmethod
	def from_json(cls, json_string):  # , module_name=None, class_name=None):
		dic = bson.json_util.loads(json_string)
		obj = cls.dict_to_obj(dic)  # , module_name=module_name, class_name=class_name):
		return obj
