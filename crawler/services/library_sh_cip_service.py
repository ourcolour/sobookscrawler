#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          library_sh_cip_service.py
@Version:       
@Time:          2020-05-25 01:46
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2020-05-25 01:46
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import re

import flask as ext
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

import configs
from services.bases.base_web_driver_service import BaseWebDriverService
from services.biz.library_sh_cip_biz import LibraryShCipBiz


class LibraryShCipService(BaseWebDriverService):
	# http://ipac.library.sh.cn/ipac20/ipac.jsp?index=ISBN&term=9787533929671
	_domain = 'ipac.library.sh.cn'
	_port = 80  # 8443

	def load_isbn_from_file(self, file_path: str) -> list:
		result = list()

		with open(file_path, 'r+') as fp:
			lines = fp.readlines()
			if lines:
				for line in lines:
					if line and len(line.strip()) > 0:
						result.append(line.strip())

		return result

	def prepare_desired_capabilities(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities['javascriptEnabled'] = True
		# capabilities['pageLoadStrategy'] = 'normal'

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

	def get_book_info_by_isbn13(self, isbn13: str) -> list:
		result = {
			'cip_list': list(),
			'pages': None,
			'thickness': None,
			'tags': list(),
			'memo': None,

			'status': True,
			'exception': None,
		}

		try:
			# Arguments
			if None is isbn13 or not isbn13.strip():
				raise ValueError('Invalid argument `isbn13`.')
			isbn13 = isbn13.strip()
			# Check ISBN13
			isbn13_regex = re.compile(r'978\d{10}')
			if not isbn13_regex.match(isbn13):
				raise ValueError('Not a valid isbn13 value: `{}`.'.format(isbn13))
			isbn13 = ext.helpers.url_quote(isbn13)

			# Format ISBN13
			formated_isbn13 = '{}-{}-{}-{}-{}'.format(
				isbn13[0:3],
				isbn13[3:4],
				isbn13[4:8],
				isbn13[8:12],
				isbn13[12:],
			)

			# Visit query form page
			self.driver.get(self.build_url(protocol='http', path='/ipac20/ipac.jsp?profile=sl'))

			# Fill query form
			self.driver = LibraryShCipBiz.fill_query_form(driver=self.driver, wait=self.wait, isbn13=isbn13)

			# Parse infos
			cip_list = LibraryShCipBiz.parse_cip_list(driver=self.driver, wait=self.wait)
			pages, thickness = LibraryShCipBiz.parse_pagination_and_thickness(driver=self.driver, wait=self.wait)
			tags = LibraryShCipBiz.parse_tag_list(driver=self.driver, wait=self.wait)
			memo = LibraryShCipBiz.parse_memo(driver=self.driver, wait=self.wait)

			# Build result
			result['cip_list'] = cip_list
			result['pages'] = pages
			result['thickness'] = thickness
			result['tags'] = tags
			result['memo'] = memo
		except Exception as ex:
			result['status'] = False
			result['exception'] = ex

		return result
