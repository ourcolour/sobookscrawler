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

from datetime import datetime

from bson import ObjectId

from crawler.entities.job_model import JobModel, S_READY, S_DRAFT, S_RUNNING, Execution
from crawler.services.biz.bases.base_mongo_biz import BaseMongoBiz


class JobMongoBiz(BaseMongoBiz[JobModel]):
	'''
	Crawler Functions
	'''

	@classmethod
	def push(cls, job_info, max_retry_count=3, **kwargs):
		# Arguments
		if None is job_info:
			raise ValueError("Invalid parameter(s) `job_info` value.")

		# Model
		model = JobModel()
		model.job_info = job_info
		# model.book_id = book_id
		# task.isbn13 = None
		# task.referer = None
		# task.status = S_DRAFT
		model.status = S_READY
		model.left_count = max_retry_count
		model.retried_count = 0
		model.executions = list()
		model.inTime = datetime.now().utcnow()
		model.editTime = None

		# Other arguments
		if None is not kwargs:
			for k, v in kwargs.items():
				if hasattr(model, k):
					setattr(model, k, v)
				else:
					print("Attribute `{}` not found in object.".format(k))
					continue

		return cls.add(model)

	@classmethod
	def update_status(cls, object_id, status, error=None):
		# Find
		if isinstance(object_id, str):
			object_id = ObjectId(object_id)
		old_model = JobModel.objects(__raw__={'_id': object_id}).first()

		# Set execution
		execution_list = [
			cls._build_execution(
				old_model.retried_count,
				'Status changed: {} -> {}'.format(old_model.status, status)
			),
		]
		if None is not error:
			execution_list.append(cls._build_execution(
				old_model.retried_count,
				'Error message: {}'.format(error)
			))
		# Assign new value
		old_model.status = status
		old_model.editTime = datetime.now().utcnow()
		for execution in execution_list:
			old_model.executions.append(execution)
		# Save to mongodb
		old_model = old_model.save()

		return old_model

	@classmethod
	def _build_execution(cls, execute_no, message):
		execution = Execution()
		execution.execute_no = execute_no
		execution.message = message
		execution.inTime = datetime.now().utcnow()
		execution.editTime = None
		return execution

	'''
	Queue Functions
	'''

	@classmethod
	def count_by_status(cls, status=S_DRAFT):
		criteria = {'status': status}
		return cls.count(criteria)

	@classmethod
	def pop(cls, status=S_READY):
		criteria = {'status': status, 'left_count': {'$gt': 0}}

		# Find one
		old_job = JobModel.objects(__raw__=criteria) \
			.order_by('editTime', '-inTime').first()

		if None is old_job:
			return None

		# Update count value
		old_job.retried_count += 1
		old_job.left_count -= 1
		print('Execution count: {} of {}'.format(old_job.retried_count, old_job.retried_count + old_job.left_count))
		# Set execution
		execution = cls._build_execution(
			old_job.retried_count,
			'Status changed: {} -> {}'.format(old_job.status, S_RUNNING)
		)
		old_job.executions.append(execution)
		old_job.status = S_RUNNING
		# old_task.status = S_READY
		old_job.editTime = datetime.now().utcnow()

		# Save to mongodb
		old_job.save()

		return old_job
