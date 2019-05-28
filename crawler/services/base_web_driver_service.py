#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          base_web_driver_service.py
@Version:       
@Time:          2019/5/23 10:15
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/23 10:15
2.  TO-DO
+-------------------------------------------------
'''

__author__ = 'cc'

import os.path
import sys
from abc import abstractmethod
import platform
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

import crawler.configs as cfg

if 'windows' == platform.system().lower():
    EXECUTABLE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'thirdparty', 'geckodriver.exe')
else:
    EXECUTABLE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'thirdparty', 'geckodriver')
DEFAULT_PROTOCOL = 'https'
DEFAULT_TIMEOUT = 3 * 1000


class BaseWebDriverService(object):
    _user_agent = UserAgent().Firefox
    # _user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'

    _domain = None
    _protocol = None

    _driver = None
    _wait = None

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def wait(self):
        return self._wait

    @wait.setter
    def wait(self, value):
        self._wait = value

    def __init__(self):
        self._init_web_driver()

        # Wait timeout
        wait_timeout = DEFAULT_TIMEOUT
        if None is cfg.TASK_WAIT_TIMEOUT or cfg.TASK_WAIT_TIMEOUT < 1:
            wait_timeout = cfg.TASK_WAIT_TIMEOUT

        self._driver.set_page_load_timeout(wait_timeout)
        self._wait = WebDriverWait(self._driver, wait_timeout)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._driver.quit()

    @abstractmethod
    def prepare_desired_capabilities(self):
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['pageLoadStrategy'] = 'eager'
        return capabilities

    @abstractmethod
    def prepare_profile(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', self._user_agent)
        return profile

    @abstractmethod
    def prepare_options(self):
        # options = webdriver.FirefoxOptions()
        # options.add_argument('--user-agent={}'.format(self._user_agent))
        return None

    def _init_web_driver(self):
        # self._driver = Firefox()
        self._driver = webdriver.Firefox(
            executable_path=EXECUTABLE_PATH,
            firefox_binary=cfg.FIREFOX_BINARY_PATH,
            desired_capabilities=self.prepare_desired_capabilities(),
            firefox_profile=self.prepare_profile(),
            firefox_options=self.prepare_options(),
            # service_log_path=None,
        )

    def build_url(self, domain=None, protocol=DEFAULT_PROTOCOL, path=None):
        if None is not protocol and len(protocol) > 0:
            self._protocol = protocol
        if None is not domain and len(domain) > 0:
            self._domain = domain

        result = '{}://{}'.format(self._protocol, self._domain)
        if None is not path and len(path) > 0:
            if '/' != path[0]:
                path = '/' + path
            result = '{}{}'.format(result, path)

        return result
