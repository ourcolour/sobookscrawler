#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          book_model.py
@Version:       
@Time:          2019-06-27 10:59
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-27 10:59
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from mongoengine import *

from crawler.entities.base_model import BaseModel

S_BASE = -2
S_DRAFT = -1
S_READY = 0
S_RUNNING = 1
S_FINISHED = 2
S_FAILED = 3

JOB_STATUS = {
	'base': S_BASE,
	'draft': S_DRAFT,
	'ready': S_READY,
	'running': S_RUNNING,
	'finished': S_FINISHED,
	'failed': S_FAILED,
}

T_BASE = 0
T_SEARCH_BY_ISBN = 1
T_FETCH_CIP_BY_ISBN = 2

JOB_TYPE = {
	'base': T_BASE,
	'search_by_isbn': T_SEARCH_BY_ISBN,
	'fetch_cip_by_isbn': T_FETCH_CIP_BY_ISBN,
}


class Execution(EmbeddedDocument):
	editTime = DateTimeField()
	inTime = DateTimeField()

	execute_no = IntField(min_value=1)
	message = StringField()


class JobInfo(EmbeddedDocument):
	book_id = IntField(min_value=1)
	isbn13 = StringField(min_length=13, max_length=13, regex=r'^978\d{10}$')
	referer = StringField(regex=r'^https?://.+$', )


class JobModel(BaseModel):
	meta = {
		'collection': 'sl_job',
	}

	status = IntField()
	executions = ListField(EmbeddedDocumentField(Execution))

	left_count = IntField(min_value=0)
	retried_count = IntField(min_value=0)

	job_type = IntField(choices=(T_SEARCH_BY_ISBN, T_FETCH_CIP_BY_ISBN, T_BASE))
	job_info = DictField()
