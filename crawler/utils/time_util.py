#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          time_util.py
@Version:       
@Time:          2019-07-29 16:00
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-07-29 16:00
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import time
from datetime import datetime

import pytz

LOCAL_FORMAT = "%Y-%m-%d %H:%M:%S"
UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

LOCAL_TZ = pytz.timezone('Asia/Shanghai')
UTC_TZ = pytz.UTC


def utc_to_local(utc_time_str, utc_format=UTC_FORMAT):
	if isinstance(utc_time_str, datetime):
		utc_time_str = utc_time_str.strftime(utc_format)

	utc_dt = datetime.strptime(utc_time_str, utc_format)
	local_dt = utc_dt.replace(tzinfo=UTC_TZ).astimezone(LOCAL_TZ)

	time_str = local_dt.strftime(LOCAL_FORMAT)

	return datetime.fromtimestamp(int(time.mktime(time.strptime(time_str, LOCAL_FORMAT))))


def local_to_utc(local_time_str, local_format=LOCAL_FORMAT):
	if isinstance(local_time_str, datetime):
		local_time_str = local_time_str.strftime(local_format)

	local_dt = datetime.strptime(local_time_str, local_format)
	utc_dt = local_dt.replace(tzinfo=LOCAL_TZ).astimezone(UTC_TZ)

	time_str = utc_dt.strftime(UTC_FORMAT)

	return datetime.fromtimestamp(int(time.mktime(time.strptime(time_str, UTC_FORMAT))))
