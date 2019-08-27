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
from crawler.services.bases.base_mongodb_service import BaseMongodbService

__author__ = 'cc'

import json
import os
import os.path
import time

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawler import configs as cfg
from crawler.services.bases.base_web_driver_service import BaseWebDriverService
from crawler.services.biz.download_task_mongo_biz import DownloadTaskMongoBiz


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
		with open(cfg.BAIDU_COOKIE_PATH, 'w+') as file_handler:
			json_string = json.dumps(cookies)
			file_handler.write(json_string)

	@classmethod
	def _load_cookies(cls, driver, wait):
		result = None

		# Whether cookie file exists
		if os.path.exists(cfg.BAIDU_COOKIE_PATH):
			try:
				# Load cookie
				with open(cfg.BAIDU_COOKIE_PATH) as file_handler:
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
				print('[ERR] method: _load_cookies(): {}', ex)
				pass

		return result

	@classmethod
	def login(cls, driver, wait, start_page=None):
		result = False

		# Redirect to login page
		# driver.get('http://ccyao.net')
		driver.get(start_page)

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
			# and set maximum wait timeout to 120 seconds.
			login_wait = WebDriverWait(driver, 120)

			# Wait until user log-in manual
			login_wait.until(EC.url_contains('disk/home'))

			# Save cookie to local json file
			cls._save_cookies(driver, wait)

			# Check login status again
			driver.refresh()
			result = cls._has_logged_in(driver, wait)

		# Save cookies if and only if login successfully
		# if result:

		return result

	@classmethod
	def save_to_yun(cls, driver, wait, download_task, netdisk_folder_name=None):
		result = False

		# Parse download task
		res_url = download_task.baiduUrl
		secret = download_task.secret

		# Fetch
		if None is res_url or not res_url:
			return result

		try:
			# Open the resource page
			driver.get(res_url)

			'''
			Check the resource existing status
			'''
			div_share_nofound_des_list = driver.find_elements_by_xpath('//div[@id="share_nofound_des"]')
			if None is not div_share_nofound_des_list and div_share_nofound_des_list:
				raise RuntimeError('Resource not exists')
			'''
			Enter secret form
			'''
			# Wait until user log-in manual
			wait.until(EC.url_contains('share/init'))

			# Fill the form with secret
			driver.find_element_by_xpath('//dd[@class="clearfix input-area"]/input[@type="text"]').send_keys(secret)

			# Submit the form by clicking
			driver.find_element_by_xpath('//dd[@class="clearfix input-area"]/div/a[@title="提取文件"]').click()

			'''
			Save file treeview form
			'''
			# Wait until save file page displayed
			wait.until(EC.presence_of_element_located((By.XPATH, '//li[@data-key="server_filename"]/div'))).click()

			# Click button [保存到网盘]
			driver.find_element_by_xpath('//a[@title="保存到网盘"]').click()

			# Wait until treeview displayed
			ul_treeview_root_content = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'treeview-root-content')))
			div_treeview_root = driver.find_element_by_class_name('treeview-root')

			# Save the treeview controls for later using
			treeview_list_item_map = {}
			treeview_list_item_array = ul_treeview_root_content.find_elements_by_tag_name('li')
			for item in treeview_list_item_array:
				treeview_list_item_map[item.text] = item

			# Find and select the treeview item by specified folder name
			if None is netdisk_folder_name or (netdisk_folder_name not in treeview_list_item_map.keys()):
				print('Target folder "{}" not found, save the resource to root node.'.format(netdisk_folder_name))
				div_treeview_root.click()
			else:
				treeview_list_item_map[netdisk_folder_name].click()

			# Find buttons
			div_dialog_footer = driver.find_element_by_class_name('dialog-footer')
			btn_confirm = div_dialog_footer.find_element_by_xpath('//a[@title="确定"]')
			unused_btn_cancel = div_dialog_footer.find_element_by_xpath('//a[@title="取消"]')
			unused_btn_new_folder = div_dialog_footer.find_element_by_xpath('//a[@title="新建文件夹"]')

			# Click button [确定]
			btn_confirm.click()

			result = True
		except Exception as ex:
			print('[ERROR] url: {}. {}'.format(res_url, ex))

		return result


class BaiduYunService(BaseWebDriverService, BaseMongodbService):
	_domain = 'pan.baidu.com'

	'''
	Initialization
	'''

	def __init__(self, alias=cfg.MONGO_CONNECTION_NAME, db=cfg.MONGO_DATABASE):
		# Init web browser
		BaseWebDriverService.__init__(self)
		# Init mongodb
		BaseMongodbService.__init__(self, alias=alias, db=db)

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		# Close web browser
		BaseWebDriverService.__exit__(self, args, kwargs)
		# Disconnect
		BaseMongodbService.__exit__(self, args, kwargs)
		pass

	def prepare_desired_capabilities(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities['javascriptEnabled'] = True
		# capabilities['pageLoadStrategy'] = 'normal'
		return capabilities

	@classmethod
	def query_tasks(cls, criteria, sort=('-publishTime', '+inTime')):
		result = DownloadTaskMongoBiz.find(criteria=criteria, sort=sort)
		return result

	def save_one(self, download_task, netdisk_folder_name='08_book_newincome'):
		result = False

		# Do login
		if not BaiduYunBiz.login(self._driver, self._wait, self.build_url()):
			raise RuntimeError('Failed to login')

		# Do saving
		result = BaiduYunBiz.save_to_yun(self._driver, self._wait, download_task, netdisk_folder_name)

		return result

	def save_many(self, download_task_list=None, netdisk_folder_name=None, skip=0):
		if None is download_task_list or not download_task_list:
			raise ValueError('No download task to run')

		# Do login
		if not BaiduYunBiz.login(self._driver, self._wait, self.build_url()):
			raise RuntimeError('Failed to login')

		# Do saving and count affected record(s)
		total = len(download_task_list)
		succeeded_list = []
		failed_list = []
		for idx, download_task in enumerate(download_task_list):
			if (idx + 1) <= skip:
				print('{:>3d}/{:>3d} [{}] 《{}》 <{}> - {}'.format(
					idx + 1,
					total,
					'SKP',
					download_task.title,
					download_task.secret,
					download_task.baiduUrl
				))
			else:
				ok = BaiduYunBiz.save_to_yun(self._driver, self._wait, download_task, netdisk_folder_name)

				if ok:
					succeeded_list.append(download_task)
				else:
					failed_list.append(download_task)

				print('{:>3d}/{:>3d} [{}] 《{}》 <{}> - {}'.format(
					idx + 1,
					total,
					' OK' if ok else 'ERR',
					download_task.title,
					download_task.secret,
					download_task.baiduUrl
				))

			time.sleep(0.2)
		print('------------------')
		print('Batch saving task finished with: {} success(es), {} failure(s).'.format(len(succeeded_list), len(failed_list)))
		print('------------------')
