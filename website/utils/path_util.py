#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          path_util.py
@Version:       
@Time:          2019-06-27 10:38
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-27 10:38
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import os
import os.path
import sys


def get_app_path():
	return os.path.join(os.path.dirname(sys.argv[0]))
