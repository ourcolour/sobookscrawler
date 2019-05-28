#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          configs.py
@Version:       
@Time:          2019/5/24 12:21
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/24 12:21
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import os.path
import sys

MONGO_HOST = 'localhost'
MONGO_PORT = 27018

MONGO_DATABASE = 'sobooks'
MONGO_COLLECTION = 'cloud_storage'
# MONGO_COLLECTION = 'download_task'

FIREFOX_BINARY_PATH = '/Applications/Firefox.app/Contents/MacOS/firefox'

TASK_WAIT_TIMEOUT = 3 * 1000

MAX_THREAD_COUNT = 1

COOKIE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'bin', 'cookie.json')
# '/Users/cc/Desktop/sobookscrawler/bin/cookie.json'
# COOKIE_PATH = '/Users/cc/Desktop/sobookscrawler/bin/cookie.json'
