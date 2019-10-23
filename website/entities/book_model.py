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

from website.entities.base_model import BaseModel


class Images(EmbeddedDocument):
	small = StringField()
	medium = StringField()
	large = StringField()


class Collections(EmbeddedDocument):
	collections = StringField()
	doings = StringField()
	wishes = StringField()


class Rating(EmbeddedDocument):
	average = FloatField(min_value=0.0, max_value=10.0)
	min = FloatField(min_value=0.0, max_value=10.0)
	max = FloatField(min_value=0.0, max_value=10.0)
	numRaters = IntField(min_value=0)
	star = FloatField(min_value=0.0, max_value=5.0)
	percents = DictField()
	# field={'0': 0.0, '1': 0.0, '2': 0.0, '3': 0.0, '4': 0.0, '5': 0.0, })
	collections = EmbeddedDocumentField(Collections)


class BookModel(BaseModel):
	meta = {
		'collection': 'sl_book_info',
	}

	author_intro = StringField()
	authors = ListField(StringField())
	binding = StringField(max_length=10)
	book_id = IntField(min_value=1)
	catalog = StringField()
	image = StringField()
	images = EmbeddedDocumentField(Images)
	isbn13 = StringField(min_length=13, max_length=13, regex=r'^9787\d{9}$', unique=True)
	origin_title = StringField()
	pages = StringField()
	price = DecimalField(min_value=1.0)
	producer = StringField()
	pubdate = DateField()
	publisher = StringField()
	rating = EmbeddedDocumentField(Rating)
	referer = StringField()
	series = StringField()
	subtitle = StringField()
	summary = StringField()
	tags = ListField(StringField())
	title = StringField()
	translator = StringField()
	url = StringField()
