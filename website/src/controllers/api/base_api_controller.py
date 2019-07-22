#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_api_controller.py
@Version:       
@Time:          2019-07-02 09:51
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-07-02 09:51
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import importlib

from flask import make_response, jsonify
from flask_restful import Resource

'''
RESTfulResponse
---------------------------
'''
INFO = 0
WARNING = INFO - 1
ERROR = INFO - 2


class RESTfulResponse(object):
	def __init__(self, code, message, data=None):
		self.code = code
		self.message = message
		self.data = data

	@classmethod
	def _build(cls, code, message, data=None):
		return RESTfulResponse(code=code, message=message, data=data)

	@classmethod
	def build_info(cls, data=None):
		return cls._build(code=INFO, message='OK', data=data)

	@classmethod
	def build_warning(cls, message='Warning', data=None):
		return cls._build(code=WARNING, message=message, data=data)

	@classmethod
	def build_error(cls, message='Error', data=None):
		return cls._build(code=ERROR, message=message, data=data)

	def to_json(self):
		return {
			'code': self.code,
			'message': self.message,
			'data': self.data,
		}

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
		if None is module_name or len(module_name) < 1:
			module_name = cls.__module__
		if None is class_name or len(class_name) < 1:
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


'''
BaseApiController
'''


class BaseApiController(Resource):
	def build_response(self, data=None, code=200):
		return make_response(jsonify(data.obj_to_dict()), code)
