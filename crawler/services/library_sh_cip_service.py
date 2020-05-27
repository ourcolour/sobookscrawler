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


class LibraryShCipService(BaseWebDriverService):
    # http://ipac.library.sh.cn/ipac20/ipac.jsp?index=ISBN&term=9787533929671
    _domain = 'ipac.library.sh.cn'
    _port = 80  # 8443

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
            if None is isbn13 or not isbn13.strip():
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
            self.driver.get(self.build_url(protocol='http', path='/ipac20/ipac.jsp?profile=sl'))

            # Fill the form
            select_control = self.driver.find_element_by_xpath('//select[@name="index"]')
            select_control.find_element_by_xpath('//option[@value="ISBN"]').click()
            self.driver.find_element_by_xpath('//input[@name="term"]').send_keys(isbn13)
            self.driver.find_element_by_xpath('//input[@type="image"]').click()

            # Fetch the cip informations
            cip_link_list = self.driver.find_elements_by_xpath(
                '//a[contains(text(),"索书号:")]/../following-sibling::td[1]//a')

            # Fetch cip_link one by one
            # and compare each one to make sure attribute `onclick` is unique
            regex = re.compile(r"(?:^(?P<cip>[^/]+)(?:[/](?P<sub>.+))?$)")
            for idx, cip_link in enumerate(cip_link_list):
                cip = cip_link.text
                m = regex.search(cip)
                if m:
                    cip = m.group(1)
                    result.append(cip)

                # print('[{:>3}] {} - {}'.format(' OK', idx + 1, cip))
            pass
        except Exception as ex:
            print('[ERR] url: {}. {}'.format(self.driver.current_url, ex))

        return result
