#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          main_sobooks.py
@Version:       
@Time:          2019/5/22 11:35
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/22 11:35
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import os

import click

from crawler.entities.crawler_task_model import S_READY, S_FAILED, S_FINISHED
from crawler.services.crawler_queue_service import CrawlerTaskService
from crawler.services.douban_book_service import DoubanBookService
from utils import path_util

# Status files
MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg')


def get_book_list(book_id_list=list()):
	# import random
	# random.shuffle(book_id_list)

	# Load book_id from text file
	with open('/Users/cc/Desktop/sobookscrawler/bin/finished.txt', 'r+') as fp:
		while True:
			try:
				line = fp.readline()

				if None is line or len(line.strip()) < 1:
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

		for book, status in book_status_list:
			if None is book:
				continue

			print('{} - {}'.format(book.id, book.url))

			with open('/Users/cc/Desktop/sobookscrawler/bin/finished.txt', 'a+') as fp:
				line = '{}\n'.format(book.book_id)
				fp.write(line)

	print('Task count: {} / {}'.format(left_count, origin_count))


def add_task(isbn13):
	"""
	Search book-info by isb13,
	then push new task into queue.

	:type isbn13: object
	"""
	# Arguments
	if None is isbn13:
		raise ValueError('Invalid `isbn13` value.')

	# Fetch process
	with CrawlerTaskService() as cts:
		with DoubanBookService() as svs:
			# Search book and fetch `book_id` list
			book_info = svs.get_book_id_by_isbn13(isbn13=isbn13)

			# Fetch book infos
			if None is not book_info and len(book_info.get('book_id_list')) > 0:
				book_id_list = book_info.get('book_id_list')
				referer = book_info.get('referer')
				print('Found {} link(s).'.format(len(book_id_list)))

				# book_status_list = svs.get_book_list(book_id_list)
				# print('2. Total {} book(s).'.format(len(book_id_list)))

				# Print fetch result
				# for book, status, ex in book_status_list:
				# 	if None is book:
				# 		continue

				for book_id in book_id_list:
					# Add book-id into queue
					if 0 < cts.count(criteria={'status': S_READY, 'book_id': book_id}):
						print('Found duplicate task, which book-id is "{}".'.format(book_id))
						continue

					task = cts.push(book_id=book_id, max_retry_count=3, referer=referer, isbn13=isbn13)
					print('< R:{} / L:{} > [book-id: {}] New task was pushed into queue.'.format(
						task.retried_count,
						task.left_count,
						task.book_id,
						task.status,
					))


def run_task(limit=5):
	# Path settings
	static_folder = 'resources'
	static_url_path = ''

	# Services
	with CrawlerTaskService() as cts:
		with DoubanBookService() as dbs:
			for i in range(0, limit):
				task = cts.pop()
				if None is task:
					print('No task in queue.')
					break

				print('< R:{} / L:{} > [book-id: {}] Task popped with status "{}".'.format(
					task.retried_count,
					task.left_count,
					task.book_id,
					task.status,
				))

				# Task - Begin ---
				try:
					# Do process
					book, status, ex = dbs.get_book_list([task.book_id])[0]  # .get_book_list(book_id_list)
					if None is not ex:
						raise ex
					# Got success, update status
					task = cts.update_status(object_id=task.id, status=S_FINISHED)
					print('< R:{} / L:{} > [book-id: {}] Fetch book from douban succeeded, {} 《{}》 - {}.'.format(
						task.retried_count,
						task.left_count,
						task.book_id,
						book.isbn13,
						book.title,
						book.authors[0] if 0 < len(book.authors) else ''
					))
					pass
				except Exception as ex:
					# Got failure, update status
					if 0 < task.left_count:
						task = cts.update_status(object_id=task.id, status=S_READY, error=ex)
					else:
						task = cts.update_status(object_id=task.id, status=S_FAILED, error=ex)
					print('< R:{} / L:{} > [book-id: {}] Task got failure, it will retry if possible.'.format(
						task.retried_count,
						task.left_count,
						task.book_id,
					))
					pass
				# Task - End -----
				pass


@click.command()
@click.option('--action', '-a', type=click.Choice(['addtask', 'runtask']))
@click.option('--isbn', type=str, default=None)  # '--action', '-a', type=str, type=click.Choice(['fetch', ], default='sobooks'))
@click.option('--limit', type=click.IntRange(1, 50, clamp=True), default=10)  # '--action', '-a', type=str, type=click.Choice(['fetch', ], default='sobooks'))
def command_dispatcher(action, isbn, limit):
	if 'addtask' == action.lower():
		isbn_list = isbn.replace(' ', '').split(',')
		for isbn in isbn_list:
			add_task(isbn)
		pass
	elif 'runtask' == action.lower():
		run_task(limit=limit)
		pass
	else:
		print('Invalid `action` value.')


if __name__ == '__main__':
	command_dispatcher()
