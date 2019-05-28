#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          sobooks_crawler_service.py
@Version:       
@Time:          2019/5/22 11:39
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/22 11:39
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import concurrent.futures
import time
from datetime import datetime

from crawler import configs
from crawler.services.base_web_driver_service import BaseWebDriverService
from crawler.services.biz.detail_page_biz import DetailPageBiz
from crawler.services.biz.download_task_mongo_biz import DownloadTaskMongoBiz


class SobooksCrawlerService(BaseWebDriverService):
	_domain = 'sobooks.cc'

	def _list_page(self, page_no=1):
		result = []

		target_url = self.build_url(path='/page/{}'.format(page_no))
		self.driver.get(target_url)

		# Verify url
		# e.g: https://sobooks.cc/page/1
		# print('PAGE: ' + self.driver.current_url)
		# if not re.match('\/page\/\\d+$', self.driver.current_url, re.I):
		# 	return result

		elements = self.driver.find_elements_by_xpath('//div[@class="card-item"]/h3/a')
		for element in elements:
			if None is element:
				continue
			href = element.get_attribute('href')
			result.append(href)

		return result

	def _detail_page(self, url, validate_code='2019777'):
		result = None

		self.driver.get(url)
		# Verify url
		# e.g: https://sobooks.cc/books/12608.html
		# print('PAGE: ' + self.driver.current_url)
		# if not re.match('\/books\/\\d+\.html', self.driver.current_url, re.I):
		# 	return result

		# Fetch detail page
		download_task = DetailPageBiz.get_book_info(driver=self.driver, wait=self.wait, validate_code=validate_code)

		# Check download url
		if self._has_download_url(download_task):
			# Check duplicate records via fields: baiduUrl or ctUrl
			old_download_task = DownloadTaskMongoBiz.find_by_url(download_task)
			if None is old_download_task:
				# Not exists do insert
				download_task.inTime = datetime.now()
				download_task.id = DownloadTaskMongoBiz.add(download_task)

				result = download_task

				return (result, 'a')
			else:
				# Exists do replace(update)
				download_task.editTime = datetime.now()
				download_task.id = old_download_task.id
				DownloadTaskMongoBiz.update_by_id(download_task.id, download_task)

				result = download_task

				return (result, 'u')
		else:
			return (result, 'e')

	# Return true if found any download url.
	def _has_download_url(self, download_task):
		if None is download_task:
			return False

		hasBaiduUrl = not (None is download_task.baiduUrl or len(download_task.baiduUrl) < 1)
		hasCtUrl = not (None is download_task.ctUrl or len(download_task.ctUrl) < 1)

		return hasBaiduUrl or hasCtUrl

	@classmethod
	def new_range_tasks(cls, from_page=1, to_page=None):
		if None is to_page or to_page < from_page or to_page < 1:
			to_page = from_page

		# Fetch every list pages in range
		with SobooksCrawlerService() as svs:
			list_page_urls = []
			for list_page_no in range(from_page, to_page):
				list_page_urls.extend(svs._list_page(list_page_no))

		# Fetch every detail pages
		# for url in list_page_urls:
		# 	download_task, code = self._detail_page(url)
		#
		# 	fmt = '{:>' + bits + 'd}/{:>' + bits + 'd} [{}]   《{}》 - {}'
		# 	print(fmt.format(
		# 		current,
		# 		total,
		# 		code.upper(),
		# 		download_task.title,
		# 		download_task.author,
		# 	))
		#
		# 	current += 1

		# Initialize
		dispatch_task_array = []
		for i in range(0, configs.MAX_THREAD_COUNT):
			dispatch_task_array.append([])

		# Seperate task
		for idx, url in enumerate(list_page_urls):
			bound = idx % configs.MAX_THREAD_COUNT
			dispatch_task_array[bound].append(url)

		# Execute task
		# current = 0
		# total = len(list_page_urls)
		# for i in range(0, MAX_THREAD_COUNT):
		# 	for url in dispatch_task_array[i]:
		# 		current += 1
		# 		print('{}/{} - IDX: {} - {}'.format(current, total, i, url))

		thread_array = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=configs.MAX_THREAD_COUNT) as executor:
			def run(thread_id, task_list):
				time.sleep(0.2)

				added = 0
				updated = 0
				error = 0

				with SobooksCrawlerService() as svs:
					# Calculate progress
					current = 1
					total = len(task_list)
					bits = str(len(str(total)))

					# Fetch every detail pages
					for url in task_list:
						download_task, code = svs._detail_page(url)

						if 'e' == code:
							fmt = 'Thread#{:>2} - {:>' + bits + 'd}/{:>' + bits + 'd} [{}]  {}'
							print(fmt.format(
								thread_id,
								current,
								total,
								code.upper(),
								'Record skipped, because of no download url found.',
							))
						else:
							fmt = 'Thread#{:>2} - {:>' + bits + 'd}/{:>' + bits + 'd} [{}]   《{}》 - {}'
							print(fmt.format(
								thread_id,
								current,
								total,
								code.upper(),
								download_task.title,
								download_task.author,
							))

						current += 1

						if 'a' == code:
							added += 1
						elif 'u' == code:
							updated += 1
						elif 'e' == code:
							error += 1

				return added, updated, error

			for i in range(0, configs.MAX_THREAD_COUNT):
				task_list = dispatch_task_array[i]
				trd = executor.submit(run, i + 1, task_list)
				thread_array.append(trd)

		for trd in concurrent.futures.as_completed(thread_array):
			try:
				added, updated, error = trd.result()
			except Exception as e:
				print('[ERR] %s' % e)
			else:
				print('[ OK] Added: {}, Update: {}, Error: {}'.format(added, updated, error))
# print('%s has %d bytes!' % (resp.url, len(resp.text)))
