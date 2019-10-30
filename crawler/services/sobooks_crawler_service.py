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
from datetime import date, datetime

import crawler.configs as cfg
from crawler.services.bases.base_mongodb_service import BaseMongodbService
from crawler.services.bases.base_web_driver_service import BaseWebDriverService
from crawler.services.biz.detail_page_biz import DetailPageBiz
from crawler.services.biz.download_task_mongo_biz import DownloadTaskMongoBiz


class SobooksCrawlerExecutor(BaseWebDriverService):

	@classmethod
	def find_duplicate_by(cls, field='referer'):
		with SobooksCrawlerService() as svs:
			duplicate_fields_dict = {}

			result_list = DownloadTaskMongoBiz.find(criteria=None, sort=field)

			for item in result_list:
				field_value = getattr(item, field)

				if field_value in duplicate_fields_dict:
					duplicate_fields_dict[field_value] += 1
				else:
					duplicate_fields_dict[field_value] = 1

				pass

			for k, v in duplicate_fields_dict.items():
				if v < 2:
					continue
				print('{} -> {}'.format(k, v))

		return

	@classmethod
	def new_range_tasks_by_detail_page_urls(cls, detail_page_urls=None):
		# Arguments
		if not detail_page_urls:
			raise ValueError('Invalid `detail_page_urls` value.')

		# Result
		thread_id = 1
		added = 0
		updated = 0
		error = 0

		# Calculate progress
		current = 1
		total = 1  # len(detail_page_urls)
		bits = 3  # str(len(str(total)))

		# Start fetching from page No.1,
		# stop until book `publishTime` great than or equal `to_date`
		with SobooksCrawlerService() as svs:
			# Fetch every detail pages
			for url in detail_page_urls:
				time.sleep(0.2)

				download_task, code = svs._detail_page(url)

				if 'e' == code:
					fmt = 'Thread#{:>2} - {:>' + str(bits) + 'd}/{:>' + str(bits) + 'd} [{}]  {}'
					print(fmt.format(
						thread_id,
						current,
						total,
						code.upper(),
						'Record skipped, because of no download url found.',
					))
				else:
					fmt = 'Thread#{:>2} - {:>' + str(bits) + 'd}/{:>' + str(bits) + 'd} [{}]   《{}》 - {}'
					print(fmt.format(
						thread_id,
						current,
						total,
						code.upper(),
						download_task.title,
						download_task.authors[0],
					))

				current += 1
				total += 1

				if 'a' == code:
					added += 1
				elif 'u' == code:
					updated += 1
				elif 'e' == code:
					error += 1

		# Print result
		print('[ OK] Added: {}, Update: {}, Error: {}'.format(added, updated, error))

		return added, updated, error

	@classmethod
	def new_range_tasks_by_publish_time(cls, to_date):
		# Arguments
		if None is to_date:
			to_date = date.today()
		if isinstance(to_date, datetime):
			to_date = to_date.date()

		# Result
		thread_id = 1
		added = 0
		updated = 0
		error = 0

		# Calculate progress
		current = 1
		total = 1  # len(detail_page_urls)
		bits = 3  # str(len(str(total)))

		# Start fetching from page No.1,
		# stop until book `publishTime` great than or equal `to_date`
		with SobooksCrawlerService() as svs:
			# From first page
			running = True
			list_page_no = 1

			# Fetching loop
			while running:
				print('Fetching list-page #{}'.format(list_page_no))

				# Fetch list pages, extract detail-page urls
				detail_page_urls = svs._list_page(list_page_no)

				# Fetch every detail pages
				for url in detail_page_urls:
					time.sleep(0.2)

					download_task, code = svs._detail_page(url)

					if 'e' == code:
						fmt = 'Thread#{:>2} - {:>' + str(bits) + 'd}/{:>' + str(bits) + 'd} [{}]  {}'
						print(fmt.format(
							thread_id,
							current,
							total,
							code.upper(),
							'Record skipped, because of no download url found.',
						))
					else:
						fmt = 'Thread#{:>2} - {:>' + str(bits) + 'd}/{:>' + str(bits) + 'd} [{}]   《{}》 - {}'
						print(fmt.format(
							thread_id,
							current,
							total,
							code.upper(),
							download_task.title,
							download_task.authors[0],
						))

					current += 1
					total += 1

					if 'a' == code:
						added += 1
					elif 'u' == code:
						updated += 1
					elif 'e' == code:
						error += 1

					# Check `publishTime`
					if download_task.publishTime.date() < to_date:
						print('Found invalid publishTime `{}` in list-page #{}, exit loop ...'.format(
							download_task.publishTime.strftime('%Y-%m-%d'),
							list_page_no
						))

						# Break while-loop
						running = False
						break

				# Next page
				list_page_no += 1

		# Print result
		print('[ OK] Added: {}, Update: {}, Error: {}'.format(added, updated, error))

		return added, updated, error

	@classmethod
	def new_tasks_by_page_range(cls, from_page=1, to_page=None):
		if None is to_page or to_page < from_page or to_page < 1:
			to_page = from_page

		# Fetch every list pages in range
		with SobooksCrawlerService() as svs:
			list_page_urls = []
			for list_page_no in range(from_page, to_page):
				list_page_urls.extend(svs._list_page(list_page_no))

		# Initialize
		dispatch_task_array = []
		for i in range(0, cfg.MAX_THREAD_COUNT):
			dispatch_task_array.append([])

		# Seperate task
		for idx, url in enumerate(list_page_urls):
			bound = idx % cfg.MAX_THREAD_COUNT
			dispatch_task_array[bound].append(url)

		thread_array = []
		with concurrent.futures.ThreadPoolExecutor(max_workers=cfg.MAX_THREAD_COUNT) as executor:
			def run(thread_id, task_list):
				time.sleep(0.2)

				added = 0
				updated = 0
				error = 0

				with SobooksCrawlerService() as svs:
					# Calculate progress
					current = 1
					total = len(task_list)
					bits = len(str(total))

					# Fetch every detail pages
					for url in task_list:
						download_task, code = svs._detail_page(url)

						if 'e' == code:
							fmt = 'Thread#{:>2} - {:>' + str(bits) + 'd}/{:>' + str(bits) + 'd} [{}]  {}'
							print(fmt.format(
								thread_id,
								current,
								total,
								code.upper(),
								'Record skipped, because of no download url found.',
							))
						else:
							fmt = 'Thread#{:>2} - {:>' + str(bits) + 'd}/{:>' + str(bits) + 'd} [{}]   《{}》 - {}'
							print(fmt.format(
								thread_id,
								current,
								total,
								code.upper(),
								download_task.title,
								download_task.authors,
							))

						current += 1

						if 'a' == code:
							added += 1
						elif 'u' == code:
							updated += 1
						elif 'e' == code:
							error += 1

				return added, updated, error

			for i in range(0, cfg.MAX_THREAD_COUNT):
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


class SobooksCrawlerService(BaseWebDriverService, BaseMongodbService):
	_domain = 'sobooks.cc'

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

	'''
	Functions
	'''

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

	def _detail_page(self, url, validate_code=cfg.SOBOOKS_VALIDATE_CODE):
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
			old_download_task = DownloadTaskMongoBiz.find_by_url(download_task.baiduUrl, download_task.ctUrl, download_task.referer)
			if None is old_download_task:
				# Not exists do insert
				result = DownloadTaskMongoBiz.add(download_task)

				return (result, 'a')
			else:
				# Exists do replace(update)
				result = DownloadTaskMongoBiz.update_by_model(old_download_task, download_task)

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
