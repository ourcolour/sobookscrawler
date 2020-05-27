#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          ccyao_service.py
@Version:       
@Time:          2019-06-12 14:19
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-12 14:19
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

import configs
from services.bases.base_web_driver_service import BaseWebDriverService


class CCYaoService(BaseWebDriverService):
	# _domain = 'httpbin.org'
	_domain = 'ccyao.net'

	# def prepare_options(self):
	# 	options = None
	# options = webdriver.FirefoxOptions()
	# options.add_argument('--proxy-server=https://{}'.format(configs.RANDOM_PROXY()))
	# options.add_argument('--user-agent={}'.format(self._user_agent))
	# return options

	# def prepare_profile(self):
	# 	profile = webdriver.FirefoxProfile()
	#
	# 	# Modify User-Agent
	# 	profile.set_preference('general.useragent.override', self._user_agent)
	#
	# 	# Modify Proxy
	# 	proxy_host, proxy_port = configs.RANDOM_PROXY()
	# 	# ---
	# 	profile.set_preference('network.proxy.type', 1)
	# 	profile.set_preference('network.proxy.http', proxy_host)
	# 	profile.set_preference('network.proxy.http_port', proxy_port)
	# 	profile.set_preference('network.proxy.ssl', proxy_host)
	# 	profile.set_preference('network.proxy.ssl_port', proxy_port)
	# 	# ---
	# 	profile.update_preferences()
	#
	# 	return profile

	def prepare_desired_capabilities(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities['javascriptEnabled'] = True
		# capabilities['pageLoadStrategy'] = 'normal'

		# Set proxy info
		proxy_string = configs.RANDOM_PROXY(False)
		proxy = Proxy()
		proxy.proxy_type = ProxyType.MANUAL
		proxy.http_proxy = proxy_string
		proxy.ssl_proxy = proxy_string
		# proxy.ftp_proxy = proxy_string
		# prox.socks_proxy = proxy_string
		proxy.add_to_capabilities(capabilities)

		return capabilities

	def visit(self):
		# Visit default page
		url = self.build_url(protocol='http')
		self.driver.get(url)

		# Display page_source
		print(self.driver.page_source)
