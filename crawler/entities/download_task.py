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

import bson
from bson import json_util
from crawler.entities.base_entity import BaseEntity


class DownloadTask(BaseEntity):
    _referer = None
    _title = None
    _authors = None
    _baiduUrl = None
    _ctUrl = None
    _publishTime = None
    _isbn = None
    _secret = None
    _formats = []
    _tags = []

    @property
    def referer(self):
        return self._referer

    @referer.setter
    def referer(self, value):
        self._referer = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def authors(self):
	    return self._authors

    @authors.setter
    def authors(self, value):
	    self._authors = value

    @property
    def baiduUrl(self):
        return self._baiduUrl

    @baiduUrl.setter
    def baiduUrl(self, value):
        self._baiduUrl = value

    @property
    def ctUrl(self):
        return self._ctUrl

    @ctUrl.setter
    def ctUrl(self, value):
        self._ctUrl = value

    @property
    def publishTime(self):
        return self._publishTime

    @publishTime.setter
    def publishTime(self, value):
        self._publishTime = value

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        self._isbn = value

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value
