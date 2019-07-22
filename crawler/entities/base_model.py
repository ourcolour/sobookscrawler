#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_model.py
@Version:       
@Time:          2019-06-27 10:57
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-27 10:57
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from mongoengine import Document
from mongoengine import ObjectIdField, DateTimeField


class BaseModel(Document):
	meta = {
		'abstract': True,
		# 'allow_inheritance': True,
	}

	# id = ObjectIdField(db_field='_id', primary_key=True)
	# id = ObjectIdField(primary_key=True)
	editTime = DateTimeField()
	inTime = DateTimeField()
