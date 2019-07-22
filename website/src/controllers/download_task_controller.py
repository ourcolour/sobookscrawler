#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          download_task_controller.py
@Version:       
@Time:          2019-06-26 14:06
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-26 14:06
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'


def index():
	return 'Hello World!'


def add_routes(app):
	app.add_url_rule('/download', view_func=index)
