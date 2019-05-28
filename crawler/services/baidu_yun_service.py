#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          baidu_yun_service.py
@Version:       
@Time:          2019/5/27 13:22
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/27 13:22
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'
import json
import os
import os.path

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawler import configs
from crawler.services.base_web_driver_service import BaseWebDriverService


class BaiduYunBiz(object):
	@classmethod
	def _has_logged_in(cls, driver, wait):
		# Check via page source
		control_list = None
		try:
			control_list = driver.find_elements_by_xpath('//span[@class="user-name"]')
		except:
			pass

		result = (None is not control_list) and (len(control_list) > 0)

		return result

	@classmethod
	def _save_cookies(cls, driver, wait):
		# Fetch cookies from web driver
		cookies = driver.get_cookies()

		# Save cookie
		with open(configs.COOKIE_PATH, 'w+') as file_handler:
			json_string = json.dumps(cookies)
			file_handler.write(json_string)

	@classmethod
	def _load_cookies(cls, driver, wait):
		result = None

		# Whether cookie file exists
		if os.path.exists(configs.COOKIE_PATH):
			try:
				# Load cookie
				with open(configs.COOKIE_PATH) as file_handler:
					# Load cookies from local json file
					cookies = json.loads(file_handler.readline())
					# Assign cookies to web driver
					driver.delete_all_cookies()
					for cookie in cookies:
						driver.add_cookie(cookie)
					# Refresh after cookies loaded
					driver.get(driver.current_url)

					result = cookies
				pass
			except Exception as ex:
				print('[ERR] method: _load_cookies(): ' + ex)
				pass

		return result

	@classmethod
	def login(cls, driver, wait):
		result = False

		# Redirect to login page
		# driver.get('http://ccyao.net')
		driver.get('https://yun.baidu.com')

		# Load cookies
		cls._load_cookies(driver, wait)

		# Check login status
		result = cls._has_logged_in(driver, wait)

		# If not logged in,
		# go on log-in action and save cookies
		if not result:
			# Redirect to login page
			driver.get(driver.current_url)

			# New a customize wait obj for user manually login action,
			# and set maximum wait timeout to 30 seconds.
			login_wait = WebDriverWait(driver, 30)

			# Wait until user log-in manual
			login_wait.until(EC.url_contains('disk/home'))

			# Save cookie to local json file
			cls._save_cookies(driver, wait)

			# Check login status again
			result = cls._has_logged_in(driver, wait)

		# Save cookies if and only if login successfully
		# if result:

		return result


class BaiduYunService(BaseWebDriverService):
	_domain = 'yun.baidu.com'

	def prepare_desired_capabilities(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities['javascriptEnabled'] = True
		# capabilities['pageLoadStrategy'] = 'normal'
		return capabilities

	def save_to_yun(self, from_url=None, to_rel_path='/'):
		# Do login first
		if not BaiduYunBiz.login(self._driver, self._wait):
			raise RuntimeError('Failed to login')

		# Fetch
		print('--- PROCESS ---')
