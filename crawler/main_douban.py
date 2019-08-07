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

from crawler.services.job_service import JobService
from utils import path_util

# Status files
MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg')


@click.command()
@click.option('--action', '-a', type=click.Choice(['addtask', 'runtask']))
@click.option('--isbn', type=str, default=None)  # '--action', '-a', type=str, type=click.Choice(['fetch', ], default='sobooks'))
@click.option('--limit', type=click.IntRange(1, 50, clamp=True), default=10)  # '--action', '-a', type=str, type=click.Choice(['fetch', ], default='sobooks'))
def command_dispatcher(action, isbn, limit):
	with JobService() as cts:
		from crawler.services.capub_cip_service import CapubCipService
		s = CapubCipService().get_cip_by_isbn13('9787559630124')
		print(s)
		return
		if 'addtask' == action.lower():
			isbn_list = isbn.replace(' ', '').split(',')
			for isbn in isbn_list:
				cts.add_task(isbn)
			pass
		elif 'runtask' == action.lower():
			cts.run_task(limit=limit)
			pass
		else:
			print('Invalid `action` value.')


if __name__ == '__main__':
	command_dispatcher()
