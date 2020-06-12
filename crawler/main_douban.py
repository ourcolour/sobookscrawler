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

# Base dir
import os
import random
import site
import time

import click

print('WORK-DIR: {}'.format(os.getcwd()))
print('SITE-PACKAGE: {}'.format(site.getsitepackages()))

from services.job_service import JobService
from services.library_sh_cip_service import LibraryShCipService
from utils import path_util

# Status files
MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg.py')


@click.command()
@click.option('--action', '-a', type=click.Choice(['addtask', 'runtask', 'querycip']))
@click.option('--isbn', type=str, default=None)
@click.option('--file', '-f', type=str, default=None)
@click.option('--limit', type=click.IntRange(1, 50, clamp=True), default=10)
def command_dispatcher(action, isbn, limit, file):
	with JobService() as cts:
		# Dispatcher
		if 'querycip' == action:
			# Cip querying method,
			# with LibraryShCipService() as svs:
			#     pass
			# A new function for cip info querying
			# added by CC.Yao 2020/05/25
			with LibraryShCipService() as svs:
				# Prepare argument `isbn`, from variable or from file.
				isbn_list = list()
				if file:
					# Load from variable
					isbn_list = svs.load_isbn_from_file(file_path=file)
				elif isbn:
					# Load from file
					isbn_list = isbn.replace(' ', '').split(',')

				for idx, isbn in enumerate(isbn_list):
					# Query book-info
					book_info = svs.get_book_info_by_isbn13(isbn13=isbn)

					# Fetch cip
					cip_list = book_info['cip_list']

					# Convert list() to string like: XXX/tabYYY/tabZZZ
					result_string = ''
					for idx, cur in enumerate(cip_list):
						if idx > 0:
							result_string += '\t'
						result_string += cur

					wait_sec = float(random.Random().randint(500, 3000)) / 1000.0
					print('[{status}]\t{wait_sec:>.2f}\t{isbn}\t{pages}\t{thickness}\t{cips}'.format(
						status=' OK' if book_info['status'] else 'ERR',
						wait_sec=wait_sec,
						isbn=isbn,
						pages=book_info['pages'],
						thickness=book_info['thickness'],
						cips=''  # ,result_string,
					))
					time.sleep(wait_sec)
				pass
			pass
		elif 'addtask' == action:
			isbn_list = isbn.replace(' ', '').split(',')
			cts.add_task(isbn_list)
			pass
		elif 'runtask' == action:
			cts.run_task(limit=limit)
			pass
		else:
			print('Invalid `action` value.')


if __name__ == '__main__':
	command_dispatcher()
