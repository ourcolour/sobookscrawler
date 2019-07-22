#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          detail_page_biz.py
@Version:       
@Time:          2019/5/22 17:04
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/22 17:04
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from crawler.entities.download_task import DownloadTask


class DetailPageBiz:
	@classmethod
	def _get_secret(cls, driver, wait, validate_code):
		input_boxes = driver.find_elements_by_xpath('//div[@class="e-secret"]/form/input[@name="e_secret_key"]')

		# Check whether need to fetch the secret code via post action
		if len(input_boxes) > 0:
			# Fill the input-box with validate code
			input_boxes[0].send_keys(validate_code)

			# Click the button
			driver.find_element_by_xpath('//div[@class="e-secret"]/form/input[@value="提交查看"]').click()

			# Wait until button submit disappear
			wait.until_not(EC.presence_of_element_located((By.XPATH, '//div[@class="e-secret"]/form/input[@value="提交查看"]')))

		secret = driver.find_element_by_xpath('//div[@class="e-secret"]/strong').text.replace('提取密码：', '')

		return secret

	@classmethod
	def get_book_info(cls, driver, wait, validate_code):
		result = DownloadTask()

		# Source page url
		result.referer = driver.current_url

		div_bookinfo_li = driver.find_elements_by_xpath('//div[@class="bookinfo"]/ul/li')
		for li in div_bookinfo_li:
			strong = li.find_element_by_tag_name('strong').text
			key = strong.replace('：', "")
			value = li.text.replace(strong, '')

			if '书名' == key:
				result.title = value
			elif '作者' == key:
				result.author = value
			elif '格式' == key:
				result.formats = value.split('/')
			elif '标签' == key:
				result.tags = value.split(' ')
			elif '时间' == key:
				result.publishTime = datetime.strptime(value, '%Y-%m-%d')
			elif 'ISBN' == key:
				result.isbn = value
			elif '浏览' == key:
				pass
			elif '评分' == key:
				pass
			else:
				raise RuntimeError('Invalid arguments: {} -> {}'.format(key, value))

		# Download link
		try:
			result.baiduUrl = driver.find_element_by_link_text('百度网盘').get_attribute('href')
			result.baiduUrl = result.baiduUrl.replace('https://sobooks.cc/go.html?url=', '')
		except:
			pass
		try:
			result.ctUrl = driver.find_element_by_link_text('城通网盘（备用）').get_attribute('href')
			result.ctUrl = result.baiduUrl.replace('https://sobooks.cc/go.html?url=', '')
		except:
			pass

		# Secret
		result.secret = cls._get_secret(driver=driver, wait=wait, validate_code=validate_code)

		return result
