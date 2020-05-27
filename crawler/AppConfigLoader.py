#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          AppConfigLoader.py
@Version:       
@Time:          2019-11-26 15:01
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-11-26 15:01
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import json
import os
from abc import ABCMeta, abstractmethod
from datetime import datetime

import configs as cfg
from utils.aliyun_acm_util import AliyunACM

SINCE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class AppConfigLoader(metaclass=ABCMeta):
	@abstractmethod
	def __init__(self, env=cfg.ACM_ENV):
		self.env = env

	@abstractmethod
	def load(self, key: str) -> dict:
		pass

	@abstractmethod
	def save(self, key: str, value: dict) -> bool:
		pass

	@abstractmethod
	def load_last_fetch(self) -> datetime:
		pass

	@abstractmethod
	def save_last_fetch(self, new_app_config: dict) -> bool:
		pass

	@abstractmethod
	def update_last_fetch(self) -> bool:
		pass


class FileAppConfigLoader(AppConfigLoader):

	def __init__(self, config_path: str = cfg.APP_CONFIG_PATH, env=cfg.ACM_ENV):
		self.env = env
		self.config_path = config_path

	def _save_file(self, file_path: str, value: dict):
		# Arguments
		if not value:
			raise ValueError('Invalid argument(s) `app_config`.')

		with open(file_path, 'w+') as file_handler:
			json.dump(value, file_handler)

		return True

	def _load_file_(self, file_path: str) -> dict:
		# Initialize the `app-config.json` if it not exists.
		if not os.path.exists(file_path):
			def _init_app_config_():
				return {
					'env': self.env,
					'last-fetch': {
						'previous_date': None,
						'current_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
					}
				}

			with open(self.config_path, 'x') as file_handler:
				json.dump(_init_app_config_(), file_handler)

		# Load the `app-config.json` file from local disk.
		app_config = None
		with open(file_path, 'r+') as file_handler:
			app_config = json.load(file_handler)

		return app_config

	def load(self, key: str) -> dict:
		app_config = self._load_file_(self.config_path)
		if not key or key not in app_config:
			return None
		return app_config[key]

	def save(self, key: str, value: dict) -> bool:
		app_config = self._load_file_(file_path=cfg.APP_CONFIG_PATH)
		app_config[key] = value
		return self._save_file(file_path=cfg.APP_CONFIG_PATH, value=app_config)

	def load_last_fetch(self) -> datetime:
		key = 'last-fetch'
		return self.load(key=key)

	def save_last_fetch(self, new_app_config: dict) -> bool:
		key = 'last-fetch'
		return self.save(key=key, value=new_app_config)

	def update_last_fetch(self) -> bool:
		key = 'last-fetch'

		# Load original one
		new_app_config = self.load(key=key).copy()

		# Update new value
		new_app_config['previous_date'] = new_app_config['current_date']
		new_app_config['current_date'] = datetime.now().strftime(SINCE_DATE_FORMAT)

		# Save new one
		if not self.save(key=key, value=new_app_config):
			raise ValueError('Failed to save to local file.')

		return new_app_config


class AliACMAppConfigLoader(AppConfigLoader):

	def __init__(self, env=cfg.ACM_ENV):
		self.env = env
		self._acm = AliyunACM(endpoint=cfg.ACM_ENDPOINT, namespace=cfg.ACM_NAMESPACE, access_key=cfg.ACM_ACCESS_KEY, secret_key=cfg.ACM_SECRET_KEY)
		self._acm.set_options(snapshot_base=cfg.ACM_SNAPSHOT_DIR)

	def load(self, key) -> dict:
		dict_content = None

		try:
			# Fetch
			content = self._acm.get(data_id=key, group=self.env)
			# Encode
			dict_content = json.loads(content)
		except:
			raise ValueError('Invalid `since-date` value from AliACM.')

		return dict_content

	def save(self, key, value: dict) -> bool:
		result = False

		try:
			# Decode
			content = json.dumps(value)
			# Publish
			result = self._acm.publish(data_id=key, content=content, group=self.env)
		except:
			raise ValueError('Invalid `since-date` value from AliACM.')

		return result

	def load_last_fetch(self) -> datetime:
		key = 'last-fetch'
		return self.load(key=key)

	def save_last_fetch(self, new_app_config: dict) -> bool:
		key = 'last-fetch'
		return self.save(key=key, value=new_app_config)

	def update_last_fetch(self) -> bool:
		key = 'last-fetch'

		# Load original one
		new_app_config = self.load(key=key).copy()

		# Update new value
		new_app_config['previous_date'] = new_app_config['current_date']
		new_app_config['current_date'] = datetime.now().strftime(SINCE_DATE_FORMAT)

		# Save new one
		if not self.save(key=key, value=new_app_config):
			raise ValueError('Failed to save to AliACM.')

		return new_app_config
