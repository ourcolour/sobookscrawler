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

from crawler.entities.download_task_model import DownloadTaskModel
from crawler.services.biz.bases.base_mongo_biz import BaseMongoBiz


class DownloadTaskMongoBiz(BaseMongoBiz[DownloadTaskModel]):

	@classmethod
	def find_by_url(cls, baiduUrl=None, ctUrl=None) -> DownloadTaskModel:
		if (None is baiduUrl or len(baiduUrl) < 1) and (None is baiduUrl or len(baiduUrl) < 1):
			raise ValueError('Invalid parameters `baiduUrl`, `ctUrl`.')

		sub_criteria = []
		if None is not baiduUrl and len(baiduUrl) > 0:
			sub_criteria.append({'baiduUrl': baiduUrl})
		if None is not ctUrl and len(ctUrl) > 0:
			sub_criteria.append({'ctUrl': ctUrl})
		criteria = {'$or': sub_criteria}

		doc = DownloadTaskModel.objects(__raw__=criteria).first()

		return doc
