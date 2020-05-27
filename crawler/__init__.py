#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          __init__.py.py
@Version:       
@Time:          2019/5/22 11:36
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/22 11:36
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

# Base dir
import os
import sys; print('Python %s on %s' % (sys.version, sys.platform))

print('SYS.PATH={}'.format(sys.path))

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.join(CUR_DIR, '..')
print(CUR_DIR)
print(WORK_DIR)
sys.path.extend([CUR_DIR, WORK_DIR])

import crawler.entities
import crawler.jobs
import crawler.services
import crawler.utils