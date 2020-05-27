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

from entities.download_task_model import DownloadTaskModel
from services.biz.bases.base_mongo_biz import BaseMongoBiz


class DownloadTaskMongoBiz(BaseMongoBiz[DownloadTaskModel]):

	@classmethod
	def find_by_url(cls, baiduUrl=None, ctUrl=None, referer=None) -> DownloadTaskModel:
		if (None is baiduUrl or not baiduUrl) \
				and (None is ctUrl or not ctUrl) \
				and (None is referer or not referer):
			raise ValueError('Invalid parameters `baiduUrl`, `ctUrl`, `referer`.')

		sub_criteria = []
		if None is not baiduUrl and baiduUrl:
			sub_criteria.append({'baiduUrl': baiduUrl})
		if None is not ctUrl and ctUrl:
			sub_criteria.append({'ctUrl': ctUrl})
		if None is not referer and referer:
			sub_criteria.append({'referer': referer})
		criteria = {'$or': sub_criteria}

		doc = DownloadTaskModel.objects(__raw__=criteria).first()

		return doc
