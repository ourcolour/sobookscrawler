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

TASK_STATUS = {
	'base': -2,
	'draft': -1,
	'ready': 0,
	'running': 1,
	'finished': 2,
	'failed': 3,
}

S_BASE = TASK_STATUS['base']
S_DRAFT = TASK_STATUS['draft']
S_READY = TASK_STATUS['ready']
S_RETRY = TASK_STATUS['ready']
S_RUNNING = TASK_STATUS['running']
S_FINISHED = TASK_STATUS['finished']
S_FAILED = TASK_STATUS['failed']


class Execution(EmbeddedDocument):
	editTime = DateTimeField()
	inTime = DateTimeField()

	execute_no = IntField(min_value=1)
	message = StringField()


class CrawlerTaskModel(BaseModel):
	meta = {
		'collection': 'sl_crawler_task',
	}

	book_id = IntField(min_value=1)
	isbn13 = StringField(min_length=13, max_length=13, regex=r'^9787\d{9}$')
	referer = StringField(regex=r'^https?://.+$', )
	status = IntField()

	left_count = IntField(min_value=0)
	retried_count = IntField(min_value=0)

	executions = ListField(EmbeddedDocumentField(Execution))
