#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          book.py
@Version:       
@Time:          2019-06-06 15:22
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-06 15:22
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from crawler.entities.base_entity import BaseEntity


class Book(BaseEntity):
	_id = None
	_alt = None
	_alt_title = None
	_author = []
	_author_intro = None
	_binding = None
	_catalog = None
	_cips = []
	_image = None
	_images = {
		'small': None,
		'medium': None,
		'large': None,
	}
	_isbn10 = None
	_isbn13 = None
	_origin_title = None
	_pages = 0
	_price = 0.0
	_pubdate = None
	_publisher = None
	_producer = None
	_rating = {
		'average': 0.0,
		'max': 0.0,
		'min': 0.0,
		'numRaters': 0,
	}
	_subtitle = None
	_summary = None
	_tags = []
	_title = None
	_translator = None
	_url = None
	_series = None

	_debug_memo = None
	_referer = None

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		self._id = value

	@property
	def alt(self):
		return self._alt

	@alt.setter
	def alt(self, value):
		self._alt = value

	@property
	def alt_title(self):
		return self._alt_title

	@alt_title.setter
	def alt_title(self, value):
		self._alt_title = value

	@property
	def author(self):
		return self._author

	@author.setter
	def author(self, value):
		self._author = value

	@property
	def author_intro(self):
		return self._author_intro

	@author_intro.setter
	def author_intro(self, value):
		self._author_intro = value

	@property
	def binding(self):
		return self._binding

	@binding.setter
	def binding(self, value):
		self._binding = value

	@property
	def catalog(self):
		return self._catalog

	@catalog.setter
	def catalog(self, value):
		self._catalog = value

	@property
	def cips(self):
		return self._cips

	@cips.setter
	def cips(self, value):
		self._cips = value

	@property
	def image(self):
		return self._image

	@image.setter
	def image(self, value):
		self._image = value

	@property
	def images(self):
		return self._images

	@images.setter
	def images(self, small=None, medium=None, large=None):
		self._images = {
			'small': small,
			'medium': medium,
			'large': large,
		}

	@property
	def isbn10(self):
		return self._isbn10

	@isbn10.setter
	def isbn10(self, value):
		self._isbn10 = value

	@property
	def isbn13(self):
		return self._isbn13

	@isbn13.setter
	def isbn13(self, value):
		self._isbn13 = value

	@property
	def origin_title(self):
		return self._origin_title

	@origin_title.setter
	def origin_title(self, value):
		self._origin_title = value

	@property
	def pages(self):
		return self._pages

	@pages.setter
	def pages(self, value):
		self._pages = value

	@property
	def price(self):
		return self._price

	@price.setter
	def price(self, value):
		self._price = value

	@property
	def pubdate(self):
		return self._pubdate

	@pubdate.setter
	def pubdate(self, value):
		self._pubdate = value

	@property
	def publisher(self):
		return self._publisher

	@publisher.setter
	def publisher(self, value):
		self._publisher = value

	@property
	def producer(self):
		return self._producer

	@producer.setter
	def producer(self, value):
		self._producer = value

	@property
	def rating(self):
		return self._rating

	@rating.setter
	def rating(self, rating):
		self._rating = rating

	@classmethod
	def build_stars_percent(cls, zero=0.0, one=0.0, two=0.0, three=0.0, four=0.0, five=0.0):
		return {
			0: zero,
			1: one,
			2: two,
			3: three,
			4: four,
			5: five,
		}

	@classmethod
	def build_rating(cls, average=0.0, min=0.0, max=0.0, num_raters=0, star=0.0, percents=None):
		return {
			'average': average,
			'min': min,
			'max': max,
			'numRaters': num_raters,
			'star': star,
			'percents': percents if None is not percents else cls.build_stars_percent(),
		}

	@property
	def subtitle(self):
		return self._subtitle

	@subtitle.setter
	def subtitle(self, value):
		self._subtitle = value

	@property
	def summary(self):
		return self._summary

	@summary.setter
	def summary(self, value):
		self._summary = value

	@property
	def tags(self):
		return self._tags

	@tags.setter
	def tags(self, value):
		self._tags = value

	@property
	def title(self):
		return self._title

	@title.setter
	def title(self, value):
		self._title = value

	@property
	def translator(self):
		return self._translator

	@translator.setter
	def translator(self, value):
		self._translator = value

	@property
	def url(self):
		return self._url

	@url.setter
	def url(self, value):
		self._url = value

	@property
	def series(self):
		return self._series

	@series.setter
	def series(self, value):
		self._series = value

	@property
	def debug_memo(self):
		return self._debug_memo

	@debug_memo.setter
	def debug_memo(self, value):
		self._debug_memo = value

	@property
	def referer(self):
		return self._referer

	@referer.setter
	def referer(self, value):
		self._referer = value
