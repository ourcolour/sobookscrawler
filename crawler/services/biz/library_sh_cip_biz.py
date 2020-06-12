#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        CC.Yao
@Contact:       ourcolour@qq.com    
@Site:          http://ccyao.net
@Project:       sobookscrawler
@File:          library_sh_cip_biz.py
@Version:       v1.0
@Time:          2020/6/12 14:33
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2020/6/12 14:33
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'CC.Yao'

import re

cip_regex = re.compile(r'(?:^(?P<cip>[^/]+)(?:[/](?P<sub>.+))?$)')
pages_regex = re.compile(r'(?:(?P<pages>(?:\d+(?:,\d+)*))页)')
thickness_regex = re.compile(r'(?:(?P<thickness>\d+(?:.\d+)?)cm)')


class LibraryShCipBiz(object):

	@classmethod
	def fill_query_form(cls, driver, wait, isbn13):
		select_control = driver.find_element_by_xpath('//select[@name="index"]')
		select_control.find_element_by_xpath('//option[@value="ISBN"]').click()
		driver.find_element_by_xpath('//input[@name="term"]').send_keys(isbn13)
		driver.find_element_by_xpath('//input[@type="image"]').click()

		return driver

	@classmethod
	def parse_cip_list(cls, driver, wait):
		result = list()

		try:
			# Fetch the cip informations
			cip_link_list = driver.find_elements_by_xpath('//a[contains(text(),"索书号:")]/../following-sibling::td[1]//a')

			# Fetch cip_link one by one
			# and compare each one to make sure attribute `onclick` is unique
			for idx, cip_link in enumerate(cip_link_list):
				cip = cip_link.text
				m = cip_regex.search(cip)
				if m:
					cip = m.group(1)
					result.append(cip)

		# print('[{:>3}] {} - {}'.format(' OK', idx + 1, cip))
		except Exception:
			pass

		return result

	@classmethod
	def parse_pagination_and_thickness(cls, driver, wait) -> (int, int):
		pages = 0
		thickness = 0

		try:
			txt = driver.find_element_by_xpath('//a[contains(text(),"载体形态:")]/../following-sibling::td[1]').text
			if txt:

				try:
					pages_txt = txt.replace(' ', '').split(';')[0]
					m = pages_regex.search(pages_txt)
					if m:
						for cur in m.groupdict()['pages'].replace(' ', '').split(','):
							pages += int(cur)
				except Exception:
					pass

				try:
					thickness_txt = txt.replace(' ', '').split(';')[1]
					m = thickness_regex.search(thickness_txt)
					if m:
						thickness = m.groupdict()['thickness'].replace(',', '')
						thickness = float(thickness)
				except Exception:
					pass
		except Exception:
			pass

		return pages, thickness

	@classmethod
	def parse_tag_list(cls, driver, wait) -> list:
		result = list()

		try:
			a_title_list = driver.find_elements_by_xpath('(//a[contains(text(),"主题标目")])[2]/../../..//a[contains(@href,"term=")]')
			for a in a_title_list:
				cur = a.get_attribute('title')
				if cur:
					tag_list = cur.strip().replace(' ', '').split('--')
					for tag in tag_list:
						if tag not in result:
							result.append(tag)
		except Exception:
			pass

		return result

	@classmethod
	def parse_memo(cls, driver, wait) -> str:
		result = None

		try:
			txt = driver.find_element_by_xpath('//a[contains(text(),"附注:")]/../following-sibling::td[1]').text
			if txt:
				result = txt.strip()
		except Exception:
			pass

		return result
