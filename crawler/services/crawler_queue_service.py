#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          crawler_queue_service.py
@Version:       
@Time:          2019-07-04 11:24
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-07-04 11:24
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from datetime import datetime

import mongoengine as me
from bson import ObjectId

import crawler.configs as cfg
from crawler.entities.crawler_task_model import CrawlerTaskModel, S_READY, S_DRAFT, S_RUNNING, Execution


class CrawlerTaskService(object):
	'''
	Initialization
	'''

	def __init__(self, alias=cfg.MONGO_DATABASE, db=cfg.MONGO_DATABASE):
		# Arguments
		self._alias = me.DEFAULT_CONNECTION_NAME  # alias
		self._db = db

		# Open database connection
		self._connection = me.connect(
			alias=self._alias,
			db=self._db,
			host=cfg.MONGO_HOST,
			port=cfg.MONGO_PORT,
		)

	def __enter__(self):
		return self

	def __exit__(self, *args):
		# Disconnect
		me.disconnect(alias=self._alias)

	'''
	Crawler Functions
	'''

	def push(self, book_id, max_retry_count=3, **kwargs):
		# Model
		task = CrawlerTaskModel()
		task.book_id = book_id
		# task.isbn13 = None
		# task.referer = None
		# task.status = S_DRAFT
		task.status = S_READY
		task.left_count = max_retry_count
		task.retried_count = 0
		task.executions = list()
		task.inTime = datetime.now()
		task.editTime = None

		# Other arguments
		if None is not kwargs:
			for k, v in kwargs.items():
				if hasattr(task, k):
					setattr(task, k, v)
				else:
					print("Attribute `{}` not found in object.".format(k))
					continue

		# Save to mongodb
		# with switch_db(CrawlerTaskModel, self._alias):
		task = task.save(alias=self._alias)

		return task

	def update(self, object_id, new_obj):
		# Find
		if isinstance(object_id, str):
			object_id = ObjectId(object_id)
		old_obj = CrawlerTaskModel.objects(__raw__={'_id': object_id}).first()

		# Assign new value
		new_obj.id = old_obj.id
		new_obj.editTime = datetime.now()

		# Save to mongodb
		return new_obj.save()

	def update_status(self, object_id, status, error=None):
		# Find
		if isinstance(object_id, str):
			object_id = ObjectId(object_id)
		old_obj = CrawlerTaskModel.objects(__raw__={'_id': object_id}).first()

		# Set execution
		execution_list = [
			self._build_execution(
				old_obj.retried_count,
				'Status changed: {} -> {}'.format(old_obj.status, status)
			),
		]
		if None is not error:
			execution_list.append(self._build_execution(
				old_obj.retried_count,
				'Error message: {}'.format(error)
			))
		# Assign new value
		old_obj.status = status
		old_obj.editTime = datetime.now()
		for execution in execution_list:
			old_obj.executions.append(execution)
		# Save to mongodb
		old_obj = old_obj.save()

		return old_obj

	def _build_execution(self, execute_no, message):
		execution = Execution()
		execution.execute_no = execute_no
		execution.message = message
		execution.inTime = datetime.now()
		execution.editTime = None
		return execution

	'''
	Queue Functions
	'''

	def count_by_status(self, status=S_DRAFT):
		criteria = {'status': status}
		return self.count(criteria)

	def count(self, criteria=dict()):
		return CrawlerTaskModel.objects(__raw__=criteria).count()

	def pop(self, status=S_READY):
		criteria = {'status': status, 'left_count': {'$gt': 0}}

		# Find one
		old_task = CrawlerTaskModel.objects(__raw__=criteria) \
			.order_by('editTime', '-inTime').first()

		if None is old_task:
			return None

		# Update count value
		old_task.retried_count += 1
		old_task.left_count -= 1
		print('Execution count: {} of {}'.format(old_task.retried_count, old_task.retried_count + old_task.left_count))
		# Set execution
		execution = self._build_execution(
			old_task.retried_count,
			'Status changed: {} -> {}'.format(old_task.status, S_RUNNING)
		)
		old_task.executions.append(execution)
		old_task.status = S_RUNNING
		# old_task.status = S_READY
		old_task.editTime = datetime.now()

		# Save to mongodb
		old_task.save()

		return old_task
