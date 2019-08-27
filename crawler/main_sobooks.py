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
from datetime import datetime

import click

from crawler.services.baidu_yun_service import BaiduYunService
from crawler.services.sobooks_crawler_service import SobooksCrawlerExecutor
from utils import path_util

# Status files
MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg')


def fetch_from_sobooks_site(since_date):
	# Arguments
	if not isinstance(since_date, datetime):
		since_date = datetime.strptime(since_date, '%Y%m%d').date()

	# Fetch newer
	SobooksCrawlerExecutor.new_range_tasks_by_publish_time(since_date)

	# def t():
	# Download newer
	with BaiduYunService() as svs:
		netdisk_folder_name = '08_book_newincome'
		from_date = datetime(since_date.year, since_date.month, since_date.day)  # datetime.strptime(since_date_str, '%Y%m%d')
		# to_date = datetime.strptime('2019-07-01', '%Y%m%d')
		# d = from_date.strftime('%Y-%m-%d')
		download_task_list = svs.query_tasks(
			criteria={'$and': [
				# {'editTime': {'$exists': 0}},
				{'publishTime': {'$gte': from_date}},
				# {'publishTime': {'$lte': to_date}},
			]}
		)

		for idx, t in enumerate(download_task_list):
			print('{:>3d}# 《{}》 {}'.format(idx + 1, t.title, t.baiduUrl))

		svs.save_many(download_task_list, netdisk_folder_name=netdisk_folder_name)


@click.command()
@click.option('--action', '-a', type=str, default='fetch')
@click.option('--since-date', '-s', type=str, default=datetime.now().strftime('%Y%m%d'),
              help='Fetch the books which `publishTime` value since (and include) since_date value')
def command_dispatcher(action, since_date):
	since_date = datetime.strptime(since_date, '%Y%m%d')
	if 'fetch' == action.lower():
		fetch_from_sobooks_site(since_date)
	else:
		print('Invalid `action` value.')


if __name__ == '__main__':
	command_dispatcher()
