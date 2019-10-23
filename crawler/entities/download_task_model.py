#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          download_task.py
@Version:       
@Time:          2019/5/22 14:08
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/22 14:08
2.  TO-DO
+-------------------------------------------------
'''
__authors__ = 'cc'

from mongoengine import *

from website.entities.base_model import BaseModel


class DownloadTaskModel(BaseModel):
	meta = {
		'collection': 'cloud_storage',
	}

	referer = StringField(regex=r'^https?://.+$', )
	title = StringField()
	author = StringField()
	authors = ListField(StringField())

	baiduUrl = StringField()
	ctUrl = StringField()
	publishTime = DateTimeField()
	# isbn = StringField(min_length=13, max_length=13, regex=r'^978\d{10}$')
	isbn = StringField()
	secret = StringField()
	formats = ListField(StringField())
	tags = ListField(StringField())
