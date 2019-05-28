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
__author__ = 'cc'

import bson
from bson import json_util


class BaseEntity(object):
    _id = None
    _inTime = None
    _editTime = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def inTime(self):
        return self._inTime

    @inTime.setter
    def inTime(self, value):
        self._inTime = value

    @property
    def editTime(self):
        return self._editTime

    @editTime.setter
    def editTime(self, value):
        self._editTime = value

    def __init__(self):
        pass

    # def __init__(self, title, author, baiduUrl, ctUrl, publishTime, inTime, isbn, secret, formats, tags):
    # 	self._title = title
    # 	self._author = author
    # 	self._baiduUrl = baiduUrl
    # 	self._ctUrl = ctUrl
    # 	self._publishTime = publishTime
    # 	self._inTime = inTime
    # 	self._isbn = isbn
    # 	self._secret = secret
    # 	self._formats = formats
    # 	self._tags = tags

    def obj_to_dict(self, needPropertyNotField=True):
        result = {}

        variables = vars(self).items()
        for k, v in variables:
            if needPropertyNotField and '_id' != k and '_' == k[:1]:
                k = k[1:]
            result[k] = v

        return result

    @classmethod
    def dict_to_obj(cls, dic):
        if None is dic:
            raise ValueError('Invalid argument.')
        result = DownloadTask()

        for (k, v) in dic.items():
            # if needPropertyNotField and '_' != k[:1]:
            # 	k = "_" + k
            setattr(result, k, v)

        return result

    def to_json(self):
        obj = self.obj_to_dict(self)
        return bson.json_util.dumps(obj)

    @classmethod
    def from_json(cls, json_string):
        dic = bson.json_util.loads(json_string)
        obj = cls.dict_to_obj(dic)
        return obj


class DownloadTask(BaseEntity):
    _referer = None
    _title = None
    _author = None
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
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

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
