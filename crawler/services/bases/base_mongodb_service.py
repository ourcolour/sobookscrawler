#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_mongodb_service.py
@Version:       
@Time:          2019-07-29 11:17
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-07-29 11:17
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import mongoengine as me

import crawler.configs as cfg


class BaseMongodbService(object):
	'''
	Initialization
	'''

	def __init__(self, alias=me.DEFAULT_CONNECTION_NAME, db=cfg.MONGO_DATABASE):
		# Arguments
		self._alias = alias  # alias
		self._db = db

		# Open database connection
		self._connection = me.connect(
			alias=self._alias,
			db=self._db,
			host=cfg.MONGO_HOST,
			# port=cfg.MONGO_PORT,
		)

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		# Disconnect
		me.disconnect(alias=self._alias)
