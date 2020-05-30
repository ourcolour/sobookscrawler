#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          detail_page_biz.py
@Version:       
@Time:          2019/5/22 17:04
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at 2019/5/22 17:04
2.  Modified at 2020/05/30 23:22
    Rewrite the detail-page fetching functions.
+-------------------------------------------------
'''
__author__ = 'cc'

import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import configs as cfg
from entities.download_task_model import DownloadTaskModel
import re


class DetailPageBiz:
    @classmethod
    def _view_secret(cls, driver, wait, validate_code):
        input_boxes = driver.find_elements_by_xpath('//div[@class="e-secret"]/form/input[@name="e_secret_key"]')

        # Check whether need to fetch the secret code via post action
        if input_boxes:
            # Fill the input-box with validate code
            input_boxes[0].send_keys(validate_code)

            # Click the button
            driver.find_element_by_xpath('//div[@class="e-secret"]/form/input[@value="提交查看"]').click()

            # Wait until button submit disappear
            wait.until_not(
                EC.presence_of_element_located((By.XPATH, '//div[@class="e-secret"]/form/input[@value="提交查看"]')))

        return

    @classmethod
    def _find_secret_element(cls, driver, wait, validate_code):
        secret_element = None

        try:
            secret_element = driver.find_element_by_xpath('//div[@class="e-secret"]/b')
        except Exception as _:
            try:
                secret_element = driver.find_element_by_xpath('//div[@class="e-secret"]/strong')
            except Exception as _:
                pass

        if not secret_element:
            # Create `screen-shot` folder if not existed
            if not os.path.exists(cfg.SCREEN_SHOT_PATH):
                os.makedirs(cfg.SCREEN_SHOT_PATH)
            # Capture error screen
            file_name = datetime.now().strftime('%Y%m%d_%H:%M:%S_%f') + '.png'
            snapshot = os.path.join(cfg.SCREEN_SHOT_PATH, file_name)
            driver.get_screenshot_as_file(snapshot)

            raise ValueError('The e-secret element not found when parsing page url: {}'.format(driver.current_url))

        return secret_element

    @classmethod
    def _get_download_info_version(cls, driver, wait):
        result = len(driver.find_elements_by_link_text('百度网盘')) \
                 + len(driver.find_elements_by_link_text('城通网盘（备用）'))
        if 0 < result:
            return 1
        else:
            return 2

    @classmethod
    def _get_download_info_v1(cls, driver, wait, validate_code):
        result = {
            'ctUrl': None,
            'baiduUrl': None,
            'secret': None,
        }

        # Secret (Parse the secret for pan.baidu.com)
        secret_element = cls._find_secret_element(driver, wait, validate_code)
        result['secret'] = secret_element.text.replace('提取密码：', '')

        # Download link
        try:
            result['baiduUrl'] = driver.find_element_by_link_text('百度网盘').get_attribute('href')
            result['baiduUrl'] = result['baiduUrl'].replace('https://sobooks.cc/go.html?url=', '')
        finally:
            pass
        try:
            result['ctUrl'] = driver.find_element_by_link_text('城通网盘（备用）').get_attribute('href')
            result['ctUrl'] = result['ctUrl'].replace('https://sobooks.cc/go.html?url=', '')
        finally:
            pass

        return result

    @classmethod
    def _get_download_info_v2(cls, driver, wait, validate_code):
        result = {
            'ctUrl': None,
            'baiduUrl': None,
            'secret': None,
        }

        # Secret (Parse the secret for pan.baidu.com)
        secret_element = cls._find_secret_element(driver, wait, validate_code)
        try:
            result['secret'] = secret_element.text[secret_element.text.index('提取码：') + 4:]
        finally:
            print('Failed to parse secret from value `{}`.'.format(secret_element.text))

        # Download link
        link_list = secret_element.find_elements_by_xpath('a')
        for link in link_list:
            cur_href = link.get_attribute('href')
            cur_href = cur_href.replace('https://sobooks.cc/go.html?url=', '')
            # CtLink
            if -1 < cur_href.find('pan.baidu.com'):
                result['baiduUrl'] = cur_href
            else:
                result['ctUrl'] = cur_href

        return result

    @classmethod
    def get_book_info(cls, driver, wait, validate_code):
        result = DownloadTaskModel()

        # Source page url
        result.referer = driver.current_url

        div_bookinfo_li = driver.find_elements_by_xpath('//div[@class="bookinfo"]/ul/li')
        for li in div_bookinfo_li:
            strong = li.find_element_by_tag_name('strong').text
            key = strong.replace('：', "")
            value = li.text.replace(strong, '')

            if '书名' == key:
                result.title = value
            elif '作者' == key:
                author_arr = list()
                if isinstance(value, str):
                    author_arr.append(value)
                else:
                    author_arr = value
                result.authors = author_arr
            elif '格式' == key:
                result.formats = value.split('/')
            elif '标签' == key:
                result.tags = value.split(' ')
            elif '时间' == key:
                result.publishTime = datetime.strptime(value, '%Y-%m-%d')
            elif 'ISBN' == key:
                result.isbn = value
            elif '浏览' == key:
                pass
            elif '评分' == key:
                pass
            elif '出版社' == key:
                pass
            else:
                raise RuntimeError('Invalid arguments: {} -> {}'.format(key, value))

        # View secret
        cls._view_secret(driver, wait, validate_code=validate_code)

        # Parse Secret
        if 1 == cls._get_download_info_version(driver, wait):
            link_info = cls._get_download_info_v1(driver, wait, validate_code)
        else:
            link_info = cls._get_download_info_v2(driver=driver, wait=wait, validate_code=validate_code)

        result.secret = link_info['secret']
        result.ctUrl = link_info['ctUrl']
        result.baiduUrl = link_info['baiduUrl']

        return result
