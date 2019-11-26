#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          aliyun_acm_util.py
@Version:       
@Time:          2019-11-25 16:25
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-11-25 16:25
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import acm


class AliyunACM(object):
	DEFAULT_GROUP = 'DEFAULT_GROUP'
	DEFAULT_TIMEOUT = None

	def __init__(self, endpoint, namespace, access_key, secret_key):
		# Variables
		self.endpoint = endpoint
		self.namespace = namespace
		self.access_key = access_key
		self.secret_key = secret_key

		# Initialize ACM instance
		self._client = acm.ACMClient(endpoint=self.endpoint, namespace=self.namespace, ak=self.access_key, sk=self.secret_key)
		pass

	def set_options(self, **kwargs):
		if kwargs:
			self._client.set_options(**kwargs)

	def get(self, data_id, group=DEFAULT_GROUP):
		return self._client.get(data_id=data_id, group=group)

	def publish(self, data_id, content, group=DEFAULT_GROUP):
		return self._client.publish(data_id=data_id, content=content, group=group)
