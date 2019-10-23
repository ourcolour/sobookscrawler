#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          sobooks_model.py
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

from website.entities.base_model import BaseModel


class SobooksModel(BaseModel):
	meta = {
		'collection': 'cloud_storage',
	}

	isbn = StringField()
	author = StringField()
	baiduUrl = StringField()
	ctUrl = StringField()
	formats = ListField(StringField())
	publishTime = DateField()
	referer = StringField()
	secret = StringField()
	tags = ListField(StringField())
	title = StringField()
