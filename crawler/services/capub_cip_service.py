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

import re

import flask as ext
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

from crawler import configs
from crawler.services.bases.base_web_driver_service import BaseWebDriverService


class CapubCipService(BaseWebDriverService):
	_domain = 'www.capub.cn'
	_port = 8443

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

	def get_cip_by_isbn13(self, isbn13: str) -> list:
		result = list()

		try:
			# Arguments
			if None is isbn13 or len(isbn13.strip()) < 1:
				raise ValueError('Invalid argument `isbn13`.')
			isbn13 = isbn13.strip()

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
			self.driver.get(self.build_url(path='/pdm/business/site/book/query/query-main.jsp'))

			# Fill the form with ISBN13 infomation
			self.driver.find_element_by_xpath('//input[@name="ISBN"]').send_keys(formated_isbn13)
			self.driver.find_element_by_link_text('查 询').click()

			# Fetch the cip informations
			cip_link_list = self.driver.find_elements_by_link_text('CIP')
			cip_id_list = list()

			# Fetch cip_link one by one
			# and compare each one to make sure attribute `onclick` is unique
			regex = re.compile(r"(?:showCipDetail\('([^']+)'\))")
			for idx, cip_link in enumerate(cip_link_list):
				onclick = cip_link.get_attribute('onclick')

				m = regex.match(onclick)
				cip_id = m.groups()[0] if m else None
				if None is cip_id:
					continue

				action = 'OK'
				if cip_id in cip_id_list:
					action = 'IGN'
				else:
					cip_id_list.append(cip_id)

				print('[{:>3}] {} - {}'.format(action, idx + 1, cip_id))

			# Click every cip link and fetch cip info
			for cip_id in cip_id_list:
				cip = self._get_cip_detail_by_cip_id(cip_id)
				result.append(cip)
			pass
		except Exception as ex:
			print('[ERR] url: {}. {}'.format(self.driver.current_url, ex))

		return result

	def _get_cip_detail_by_cip_id(self, cip_id: str) -> str:
		result = None

		try:
			# Visit cip detail page
			self.driver.get(self.build_url(path='/pdm/business/queryCipAction.do?method=doSrchDetail&cipid={}'.format(cip_id)))
			td_cip = self.driver.find_element_by_xpath('//table[@class="bizform"]/tbody/tr/td[contains(text(),"中图法分类")]/following-sibling::td')
			result = td_cip.text
		except Exception as ex:
			print(ex)

		return result
