#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          job_service.py
@Version:       
@Time:          2019-07-04 11:24
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-07-04 11:24
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from crawler.entities.job_model import S_READY, S_FAILED, S_FINISHED
from crawler.services.bases.base_mongodb_service import BaseMongodbService
from crawler.services.biz.job_mongo_biz import JobMongoBiz
from crawler.services.douban_book_service import DoubanBookService


class JobService(BaseMongodbService):

	def test(self):
		# from crawler.entities.crawler_task_model import CrawlerTaskModel
		# rs = CrawlerTaskModel.objects(__raw__={})
		rs = JobMongoBiz.count(criteria={})
		print(rs.count())

	def add_task(self, isbn13):
		"""
		Search book-info by isb13,
		then push new task into queue.

		:type isbn13: object
		"""
		# Arguments
		if None is isbn13:
			raise ValueError('Invalid `isbn13` value.')

		# Fetch process
		with DoubanBookService() as svs:
			# Search book and fetch `book_id` list
			book_info = svs.get_book_id_by_isbn13(isbn13=isbn13)

			# Fetch book infos
			if None is not book_info and book_info.get('book_id_list'):
				book_id_list = book_info.get('book_id_list')
				referer = book_info.get('referer')
				print('Found {} link(s).'.format(len(book_id_list)))

				for book_id in book_id_list:
					# Add book-id into queue
					job_info = {
						'book_id': book_id,
						'referer': referer,
						'isbn13': isbn13,
					}
					if 0 < JobMongoBiz.count(criteria={'status': S_READY, 'job_info': job_info}):
						print('Found duplicate task, which book-id is "{}".'.format(book_id))
						continue

					job = JobMongoBiz.push(job_info=job_info, max_retry_count=3)
					print('< R:{} / L:{} > [book-id: {}] New task was pushed into queue.'.format(
						job.retried_count,
						job.left_count,
						job.job_info['book_id']
					))
					pass

	def run_task(self, limit=5):
		# Services
		with DoubanBookService() as dbs:
			for _ in range(0, limit):
				job = JobMongoBiz.pop()
				if None is job:
					print('No task in queue.')
					break

				print('< R:{} / L:{} > [book-id: {}] Task popped with status "{}".'.format(
					job.retried_count,
					job.left_count,
					job.job_info['book_id'],
					job.status
				))

				# Task - Begin ---
				try:
					# Do process
					book, status, ex = dbs.get_book_list([job.job_info['book_id']])[0]
					if None is not ex:
						raise ex
					# Got success, update status
					job = JobMongoBiz.update_status(object_id=job.id, status=S_FINISHED)
					print('< R:{} / L:{} > [book-id: {}] Fetch book from douban succeeded, {} 《{}》 - {}.'.format(
						job.retried_count,
						job.left_count,
						job.job_info['book_id'],
						book.isbn13,
						book.title,
						book.authors[0] if book.authors else ''
					))
					pass
				except Exception as ex:
					# Got failure, update status
					if 0 < job.left_count:
						job = JobMongoBiz.update_status(object_id=job.id, status=S_READY, error=ex)
					else:
						job = JobMongoBiz.update_status(object_id=job.id, status=S_FAILED, error=ex)
					print('< R:{} / L:{} > [book-id: {}] Task got failure, it will retry if possible.'.format(
						job.retried_count,
						job.left_count,
						job.job_info['book_id'],
					))
					pass
				# Task - End -----
				pass

	def get_book_list(self, book_id_list=None):
		if None is book_id_list:
			book_id_list = list()

		# import random
		# random.shuffle(book_id_list)

		# Load book_id from text file
		with open('/Users/cc/Desktop/sobookscrawler/bin/finished.txt', 'r+') as fp:
			while True:
				try:
					line = fp.readline()

					if None is line or not line.strip():
						raise EOFError()

					line = line.strip()

					if line in book_id_list:
						book_id_list.remove(line)
						print('[SKP] {}'.format(line))
				except EOFError as ex:
					print(ex)
					break

		# Count tasks
		task_count = 10
		origin_count = len(book_id_list)
		left_count = origin_count - task_count
		if left_count < 1:
			left_count = 0

		print('Task count: {} / {}'.format(left_count, origin_count))
		print('Fetch next {} tasks.'.format(task_count))

		book_id_list = book_id_list[:task_count]
		with DoubanBookService() as svs:
			book_status_list = svs.get_book_list(book_id_list)
			print('Total {} book(s).'.format(len(book_id_list)))

			for book, unused_status in book_status_list:
				if None is book:
					continue

				print('{} - {}'.format(book.id, book.url))

				with open('/Users/cc/Desktop/sobookscrawler/bin/finished.txt', 'a+') as fp:
					line = '{}\n'.format(book.book_id)
					fp.write(line)

		print('Task count: {} / {}'.format(left_count, origin_count))
