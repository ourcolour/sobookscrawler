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

import json
import os.path
import platform
import random
import sys
from datetime import datetime

import mongoengine as me

from crawler.utils import path_util

rnd = random.Random()

HTTPS_PROXY_LIST = [
	# '122.193.246.218:9999',
	# '112.85.164.143:9999',
	# '61.174.154.166:4204',
	'60.188.52.91:4274',
	# '220.185.12.195:4276',
	# '115.237.91.237:5946',
	# '115.239.20.194:2549',
	'115.211.37.26:4230',
	'125.111.150.229:4205',
	'60.186.255.165:1246',
	'183.145.63.28:5946',
	'115.221.11.21:4212',
]


def RANDOM_PROXY(return_tuple=True):
	idx = rnd.randint(0, len(HTTPS_PROXY_LIST) - 1)
	result = HTTPS_PROXY_LIST[idx]

	if return_tuple:
		arr = result.split(':')
		return arr[0], int(arr[1])
	else:
		return result


# MONGO_HOST = 'mongodb://127.0.0.1:27018' #'192.168.2.91'
MONGO_HOST = 'mongodb://mongo01.dev.xjh.com:27017,mongo02.dev.xjh.com:27017,mongo03.dev.xjh.com:27017/?replicaSet=xjh'
MONGO_PORT = 27018

MONGO_CONNECTION_NAME = me.DEFAULT_CONNECTION_NAME
MONGO_DATABASE = 'DoubanBookApi'
# MONGO_COLLECTION = 'cloud_storage'
# MONGO_COLLECTION = 'download_task'

FIREFOX_BINARY_PATH = '/Applications/Firefox.app/Contents/MacOS/firefox'

TASK_WAIT_TIMEOUT = 3 * 1000

MAX_THREAD_COUNT = 1

APP_CONFIG_PATH = os.path.join(path_util.get_app_path(), '..', 'bin', 'app-config.json')

BAIDU_COOKIE_PATH = os.path.join(path_util.get_app_path(), '..', 'bin', 'baidu-cookie.json')
# '/Users/cc/Desktop/sobookscrawler/bin/baidu-cookie.json'
# COOKIE_PATH = '/Users/cc/Desktop/sobookscrawler/bin/baidu-cookie.json'
DOUBAN_COOKIE_PATH = os.path.join(os.path.dirname(sys.argv[0]), '..', 'bin', 'douban-cookie.json')

if 'windows' == platform.system().lower():
	GECKO_EXECUTABLE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'thirdparty', 'geckodriver.exe')
else:
	GECKO_EXECUTABLE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'thirdparty', 'geckodriver')
print('Geckodriver: {}'.format(GECKO_EXECUTABLE_PATH))

SOBOOKS_VALIDATE_CODE = '20190808'


# ----------
# DO NOT MODIFY THE INFOMATIONS BELOW
# ----------
def save_app_config(app_config_dict):
	# Arguments
	if not app_config_dict:
		raise ValueError('Invalid argument(s) `app_config`.')

	with open(APP_CONFIG_PATH, 'w+') as file_handler:
		json_string = json.dumps(app_config_dict)
		file_handler.write(json_string)

	pass


def load_app_config() -> dict:
	# Initialize the `app-config.json` if it not exists.
	if not os.path.exists(APP_CONFIG_PATH):
		def _init_app_config_():
			return {
				'since_date': {
					'previous_date': None,
					'current_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
				}
			}

		with open(APP_CONFIG_PATH, 'x') as file_handler:
			json_string = json.dumps(_init_app_config_())
			file_handler.write(json_string)

	# Load the `app-config.json` file from local disk.
	app_config = None
	with open(APP_CONFIG_PATH, 'r+') as file_handler:
		lines = file_handler.readline()
		app_config = json.loads(lines)

	return app_config
