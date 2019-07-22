#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          douban_book_service.py
@Version:       
@Time:          2019-06-06 15:00
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-06 15:00
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import random
import re
import time

import flask as ext
from prettytable import PrettyTable
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

from crawler import configs
from crawler.entities.book import Book
from crawler.services.base_web_driver_service import BaseWebDriverService
from crawler.services.biz.book_mongo_biz import BookMongoBiz
from crawler.services.biz.douban_book_biz import DoubanBookBiz


class DoubanBookService(BaseWebDriverService):
	_domain = 'book.douban.com'

	def prepare_desired_capabilities(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities['javascriptEnabled'] = True
		# capabilities['pageLoadStrategy'] = 'normal'
		capabilities['pageLoadStrategy'] = 'normal'

		# Set proxy
		proxy_string = configs.RANDOM_PROXY(return_tuple=False)
		proxy = Proxy()
		proxy.proxy_type = ProxyType.MANUAL
		proxy.http_proxy = proxy_string
		proxy.ssl_proxy = proxy_string
		# proxy.ftp_proxy = proxy_string
		# prox.socks_proxy = proxy_string
		# proxy.add_to_capabilities(capabilities)

		return capabilities

	def find_duplicate_by(self, field='isbn13'):
		result = []

		duplicate_fields_dict = {}
		book_list = BookMongoBiz.find(filter=None, sort=(field, 1))
		for book in book_list:
			# author_str = ''
			# for a in book.authors:
			# 	if len(author_str) > 0:
			# 		author_str += ', '
			# 	author_str += a
			# print('{} -《{}》 {}'.format(book.isbn13, book.title, author_str))

			field_value = getattr(book, field)
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

	def get_book_id_by_isbn13(self, isbn13):
		# https://book.douban.com/subject_search?search_text=%3Cisbn%3E&cat=1001
		result = list()

		try:
			# Arguments
			if None is isbn13 or len(isbn13.strip()) < 1:
				raise ValueError('Invalid argument `isbn13`.')
			isbn13 = isbn13.strip()

			isbn13_regex = re.compile(r'9787\d{9}')
			if not isbn13_regex.match(isbn13):
				raise ValueError('Not a valid isbn13 value: `{}`.'.format(isbn13))

			# Visit search page
			isbn13 = ext.helpers.url_quote(isbn13)
			self.driver.get(self.build_url(path='/subject_search?search_text={}&cat=1001'.format(isbn13)))

			# Build regex
			book_id_regex = re.compile(r'^' + self.build_url(path='/subject/') + r'(\d+)/$', re.I)

			# Fetch all items
			title_link_list = self.driver.find_elements_by_class_name('title-text')
			for link in title_link_list:
				if None is link:
					continue

				# href="https://book.douban.com/subject/25987952/"
				href = link.get_attribute('href')
				# Fetch `book_id` value via regex
				m = book_id_regex.match(href)
				if m:
					book_id = int(m.groups()[0])
					if book_id > 0:
						result.append(book_id)
					else:
						print('Invalid href: {}'.format(href))
		except Exception as ex:
			print('[ERR] url: {}. {}'.format(self.driver.current_url, ex))

		return {
			'book_id_list': result,
			'isbn13': isbn13,
			'referer': self.driver.current_url,
		}

	def get_book_list(self, book_id_list):
		result = list()

		# Fetch books
		rnd = random.Random()
		for book_id in book_id_list:
			result.append(self.get_book(book_id))

			# Sleep a while
			sec_to_sleep = rnd.randint(1, 5)
			print('Sleep {} second(s).'.format(sec_to_sleep))
			time.sleep(sec_to_sleep)

		# Initialize table # 'authors',
		tbl = PrettyTable()
		# , 'title'
		tbl.field_names = ['isbn13', 'basic', 'intro', 'tags', 'rating', '--all--', 'db-action', 'message']
		# Set align
		tbl.align['title'] = 'l'

		# Prepare table row
		for book, status_dict, ex in result:
			# Prepare content
			column_values = list()
			for column in tbl.field_names:
				display = None

				if 'isbn13' == column:
					display = book.isbn13
				elif 'title' == column:
					display = book.title
				elif 'authors' == column:
					display = ''
					if None is not book.authors and len(book.authors) > 0:
						display = book.authors[0]
						if len(book.authors) > 1:
							display += ' ...'
				elif 'db-action' == column:
					display = status_dict['db-action']
				elif 'message' == column:
					display = status_dict['message']
				elif column in status_dict.keys():
					status = status_dict.get(column)
					if status:
						display = '○'  # '●○√'
					else:
						display = '×'  # '×'
				else:
					continue
				column_values.append(display)
				pass
			tbl.add_row(column_values)

		# Print
		print(tbl)

		return result

	def get_book(self, book_id):
		result = None
		status_dict = dict()
		ex = None

		try:
			# Visit info page
			self.driver.get(self.build_url(path='/subject/{}/'.format(book_id)))

			# New book instance
			result = Book()
			result.book_id = book_id
			result.referer = self.driver.current_url
			result.url = self.driver.current_url

			# Initialize status_dict
			status_dict['basic'] = False
			status_dict['intro'] = False
			status_dict['tags'] = False
			status_dict['rating'] = False
			status_dict['--all--'] = False
			status_dict['message'] = '-'
			status_dict['db-action'] = '-'

			# Basic info
			status_dict['basic'] = DoubanBookBiz.get_basic_info(self.driver, self.wait, result)
			# Intro info
			status_dict['intro'] = DoubanBookBiz.get_intro_info(self.driver, self.wait, result)
			# Tags info
			status_dict['tags'] = DoubanBookBiz.get_tags_info(self.driver, self.wait, result)
			# Rating info
			status_dict['rating'] = DoubanBookBiz.get_rating_info(self.driver, self.wait, result)

			# Visit comment page
			self.driver.get(self.build_url(path='/subject/{}/collections'.format(book_id)))
			# Collections info
			status_dict['collections'] = DoubanBookBiz.get_collections_info(self.driver, self.wait, result)

			status_dict['--all--'] = True
			for ok in status_dict.values():
				if not ok:
					status_dict['--all--'] = False
					break

			status_dict['message'] = '-'
			status_dict['db-action'] = '-'
			if status_dict['--all--']:
				# Check existance by isbn13
				old_book = BookMongoBiz.find_one(filter={'isbn13': result.isbn13})
				if None is not old_book:
					result, affected = BookMongoBiz.update_by_entity(Book.dict_to_obj(old_book), result)
					status_dict['db-action'] = 'U'
				else:
					result = BookMongoBiz.add(result)
					status_dict['db-action'] = 'A'
			else:
				status_dict['message'] = 'Got error during get_book'
				raise Exception(status_dict['message'])
		except Exception as exc:
			ex = exc
			print('[ERR] url: {}. {}'.format(self.driver.current_url, ex))

		return result, status_dict, ex

	def save_book(self, book):
		return BookMongoBiz.add(book)
