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
from datetime import datetime, date

import click

import crawler.configs as cfg
from crawler.services.baidu_yun_service import BaiduYunService
from crawler.services.sobooks_crawler_service import SobooksCrawlerExecutor
from website.utils import path_util

# Status files
# MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg.py')

APP_CONFIG = cfg.load_app_config()
SINCE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def fetch_from_sobooks_site(since_date=None):
	def _save_since_date_into_app_config_():
		new_app_config = APP_CONFIG.copy()
		new_app_config['since_date']['previous_date'] = APP_CONFIG['since_date']['current_date']
		new_app_config['since_date']['current_date'] = datetime.now().strftime(SINCE_DATE_FORMAT)
		cfg.save_app_config(new_app_config)

	def _load_since_date_from_app_config_():
		# Parse `since_date` value from `APP_CONFIG` dict.
		since_date = APP_CONFIG['since_date']['current_date']

		# Convert to date type.
		if not isinstance(since_date, date):
			since_date = datetime.strptime(since_date, SINCE_DATE_FORMAT).date()

		return since_date

	# urls = []
	# SobooksCrawlerExecutor.new_range_tasks_by_detail_page_urls(detail_page_urls=urls)
	# return

	# SobooksCrawlerExecutor.find_duplicate_by(field='baiduUrl')
	# return

	# Arguments
	if not since_date:
		since_date = _load_since_date_from_app_config_()
	if not isinstance(since_date, date):
		since_date = datetime.strptime(since_date, SINCE_DATE_FORMAT).date()

	# Fetch newer
	SobooksCrawlerExecutor.new_range_tasks_by_publish_time(since_date)
	# return

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

		name_arr = [
			'脑髓地狱', '发现的乐趣', '名著名译丛书（第五辑）', '第一推动丛书·生命系列（套装共5册）', '跨市场交易策略（典藏版）', '亡者归来', '地狱书单', '茶叶大盗', '成化十四年', '人人都该懂的克隆技术', '罪与罚（名著名译丛书）', '仲夏夜之梦（莎士比亚戏剧中文版）', '巴黎美人', '晋江大神Priest经典作品合集（套装10册）', '国史论衡', '被偷走的人生', '技巧：如何用一年时间获得十年的经验', '晚清中国的光与影', '征途美国',
			'世界因何美妙而优雅地运行',
		]
		# Remove task
		print('Total count: {}'.format(len(download_task_list)))
		new_download_task_list = list()
		for task in download_task_list:
			# if task.title in name_arr:
			new_download_task_list.append(task)
		print('Total count: {}'.format(len(new_download_task_list)))
		svs.save_many(new_download_task_list, netdisk_folder_name=netdisk_folder_name)

	# Update `APP_CONFIG` with new `since_date` value
	_save_since_date_into_app_config_()


@click.command()
@click.option('--action', '-a', type=str, default='fetch')
@click.option('--since-date', '-s', type=str, default='', help='Fetch the books which `publishTime` value since (and include) since_date value')
def command_dispatcher(action, since_date):
	if since_date == '':
		since_date = None
	else:
		since_date = datetime.strptime(since_date, '%Y%m%d')
	if 'fetch' == action.lower():
		fetch_from_sobooks_site(since_date)
	else:
		print('Invalid `action` value.')


if __name__ == '__main__':
	command_dispatcher()
