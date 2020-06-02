#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          douban_book_biz.py
@Version:       
@Time:          2019-06-11 14:07
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-11 14:07
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import json
import os
import re
import sys
from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import configs


class DoubanBookBiz(object):
    @classmethod
    def _save_cookies(cls, driver, wait):
        # Fetch cookies from web driver
        cookies = driver.get_cookies()

        # Save cookie
        with open(configs.DOUBAN_COOKIE_PATH, 'w+') as file_handler:
            json_string = json.dumps(cookies)
            file_handler.write(json_string)

    @classmethod
    def _load_cookies(cls, driver, wait):
        result = None

        # Whether cookie file exists
        if os.path.exists(configs.DOUBAN_COOKIE_PATH):
            try:
                # Load cookie
                with open(configs.DOUBAN_COOKIE_PATH) as file_handler:
                    # Load cookies from local json file
                    cookies = json.loads(file_handler.readline())
                    # Assign cookies to web driver
                    driver.delete_all_cookies()
                    for cookie in cookies:
                        if cookie['domain'].find('www.') > -1:
                            cookie['domain'] = cookie['domain'].replace('www.', '.')
                        driver.add_cookie(cookie)
                    # Refresh after cookies loaded
                    driver.get(driver.current_url)

                    result = cookies
                pass
            except Exception as ex:
                print('[ERR] method: _load_cookies(): ' + ex)
                pass

        return result

    @classmethod
    def handle_ip_error(cls, driver, wait) -> bool:
        result = False

        # Check via page source
        got_error = -1 < driver.current_url.find("sec.douban.com")

        if got_error:
            # Do log in action
            result = cls.login(driver, wait, start_page=driver.current_url)

        return result

    @classmethod
    def _has_logged_in(cls, driver, wait) -> bool:
        return len(driver.find_elements_by_link_text('提醒')) > 0

    @classmethod
    def login(cls, driver, wait, start_page=None, login_page=None) -> bool:
        result = False

        # Redirect to start page
        if start_page:
            driver.get(start_page)

        # Load cookies
        cls._load_cookies(driver, wait)

        # Check login status
        result = cls._has_logged_in(driver, wait)

        # If not logged in,
        # go on log-in action and save cookies
        if not result:
            # Redirect to login page
            if login_page:
                driver.get(login_page)

            # New a customize wait obj for user manually login action,
            # and set maximum wait timeout to 120 seconds.
            login_wait = WebDriverWait(driver, 120)

            # Wait until user log-in manual
            login_wait.until(EC.presence_of_element_located((By.LINK_TEXT, '提醒')))

            # Save cookie to local json file
            cls._save_cookies(driver, wait)

            # Check login status again
            result = cls._has_logged_in(driver, wait)
            # If logged in, redirect to start page
            if result:
                # Redirect to start page
                if start_page:
                    driver.get(start_page)

        return result

    @classmethod
    def get_intro_info(cls, driver, wait, ref_book) -> bool:
        result = True

        # Expend all book info before fetch
        a_expand_list = driver.find_elements_by_link_text('(展开全部)')
        a_more_list = driver.find_elements_by_link_text('更多')
        a_list = a_expand_list
        a_list.extend(a_more_list)
        # print('Found links: {}, include 展开全部: {} 更多: {} .'.format(
        # 	len(a_list),
        # 	len(a_expand_list),
        # 	len(a_more_list)
        # ))

        for a in a_list:
            if None is not a:
                try:
                    # Scroll to the view and move to the element
                    # to make sure target element 'hover' state,
                    # then perform 'click' action.
                    driver.execute_script("arguments[0].scrollIntoView(false);", a)
                    ActionChains(driver).move_to_element(a).click().perform()
                except Exception as ex:
                    target_dir = os.path.join(os.path.dirname(sys.argv[0], 'bin', 'screenshot'))
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    prefix = ref_book.id + '_' + datetime.strftime('%Y%m%d_%H%M%S')
                    snapshot_path = '{}.{}'.format(prefix, 'png')
                    html_path = '{}.{}'.format(prefix, 'html')

                    print('Save snapshot: {}'.format(driver.save_screenshot(snapshot_path)))
                    with open(html_path, 'w+') as fp:
                        fp.write(driver.page_source)
                    print('Got exception during clicking "Expanding links"' + ex)

                    result = False
                    pass

        # Related info (内容简介 / 作者简介 / 目录)
        h2_span_list = driver.find_elements_by_xpath('//div[@class="related_info"]/h2')
        for h2_span in h2_span_list:
            h2_span_text = h2_span.text.replace('  · · · · · ·', '').strip()
            if '内容简介' == h2_span_text:
                ref_book.summary = h2_span.find_element_by_xpath('following-sibling::div').text
            elif '作者简介' == h2_span_text:
                ref_book.author_intro = h2_span.find_element_by_xpath('following-sibling::div').text
            elif '目录' == h2_span_text:
                ref_book.catalog = h2_span.find_element_by_xpath('following-sibling::div').text
            elif re.match(r'^"[^"]+"试读$', h2_span_text):
                pass
            else:
                print('H2 "{}" was not unsupported.'.format(h2_span_text))
                result = False

        return result

    @classmethod
    def get_rating_info(cls, driver, wait, ref_book) -> bool:
        result = True

        # Default value
        num_raters = 0
        rating_average = 0.0
        # rating_min = 0.0
        rating_max = 0.0
        percent_dict = ref_book.build_stars_percent()
        star = 0

        # If exists rating
        if not driver.find_elements_by_link_text('评价人数不足') \
                and not driver.find_elements_by_xpath('//div[@class="rating_sum"]/span[contains(text(),"目前无人评价")]'):
            rating_max = float(driver.find_element_by_xpath('//span[@property="v:best"]').get_attribute('content'))
            rating_average = float(driver.find_element_by_xpath('//strong[@property="v:average"]').text)
            num_raters = int(driver.find_element_by_xpath('//span[@property="v:votes"]').text)

            # Average star

            for i in range(50, -1, -5):
                if driver.find_elements_by_class_name('bigstar{}'.format(i)):
                    star = i
                    break
            star = star / 10.0

            # Rating percent for different star level
            rating_per_element_list = driver.find_elements_by_class_name('rating_per')
            count = len(rating_per_element_list)
            for i in range(0, count):
                no_str = str(count - i)
                percent_dict['{}'.format(no_str)] = float(rating_per_element_list[i].text.replace('%', '').strip())
        else:
            pass
        # print('目前无人评价')

        # Assign values
        ref_book.rating = ref_book.build_rating(
            average=rating_average,
            max=rating_max,
            num_raters=num_raters,
            star=star,
            percents=percent_dict
        )

        return result

    @classmethod
    def get_tags_info(cls, driver, wait, ref_book) -> bool:
        result = True

        # Initialize field `tags`
        if None is ref_book.tags:
            ref_book.tags = list()

        # Fetch tags info
        tag_element_array = driver.find_elements_by_xpath('//div[@id="db-tags-section"]/div/span/a')
        for tag_element in tag_element_array:
            tag = ref_book.build_tags(name=tag_element.text, title=tag_element.text, count=0)
            ref_book.tags.append(tag)

        return result

    @classmethod
    def get_collections_info(cls, driver, wait, ref_book) -> bool:
        result = True

        try:
            # Fetch collections info
            collections = int(
                driver.find_element_by_xpath('//span[@id="collections_bar"]/span').text.replace('人', '').replace('读过',
                                                                                                                 '').strip())
            doings = int(
                driver.find_element_by_xpath('//span[@id="doings_bar"]/span').text.replace('人', '').replace('在读',
                                                                                                            '').strip())
            wishes = int(
                driver.find_element_by_xpath('//span[@id="wishes_bar"]/span').text.replace('人', '').replace('想读',
                                                                                                            '').strip())

            # Assign value
            ref_book.rating['collections'] = ref_book.build_collections(wishes=wishes, doings=doings,
                                                                        collections=collections)
            pass
        except Exception as ex:
            result = False
            print(ex)

        return result

    @classmethod
    def get_basic_info(cls, driver, wait, ref_book) -> bool:
        result = True

        # Title
        ref_book.title = driver.find_element_by_xpath('//h1/span').text

        # Images
        # e.g.: https://img3.doubanio.com/view/subject/m/public/s32332471.jpg
        ref_book.image = driver.find_element_by_xpath('//div[@id="mainpic"]/a').get_attribute('href')
        ref_book.images = ref_book.build_images(
            large=ref_book.image,
            medium=ref_book.image.replace('/subject/l/public/', '/subject/m/public/'),
            small=ref_book.image.replace('/subject/l/public/', '/subject/s/public/')
        )

        # Other info
        try:
            info_array = driver.find_element_by_xpath('//div[@id="info"]').text.split('\n')
            for info in info_array:
                if None is info:
                    continue
                kv_arr = info.strip().split(': ')
                if len(kv_arr) < 2:
                    continue

                ok = True
                key = kv_arr[0].strip()
                value = kv_arr[1].strip()

                if '作者' == key:
                    if None is ref_book.authors:
                        ref_book.authors = []

                    v_arr = value.split('/')
                    for v in v_arr:
                        v = v.strip()
                        if None is v or not v:
                            continue
                        ref_book.authors.append(v)
                elif '出版社' == key:
                    ref_book.publisher = value
                elif '出品方' == key:
                    ref_book.producer = value
                elif '原作名' == key:
                    ref_book.origin_title = value
                elif '副标题' == key:
                    ref_book.subtitle = value
                elif '译者' == key:
                    ref_book.translator = value
                elif '出版年' == key:
                    fmt = None
                    if re.match(r'^\d{4}-\d{1,2}-\d{1,2}$', value):
                        fmt = '%Y-%m-%d'
                    elif re.match(r'^\d{4}-\d{1,2}$', value):
                        fmt = '%Y-%m'
                    if None is not fmt:
                        ref_book.pubdate = datetime.strptime(value, fmt)
                    pass
                elif '页数' == key:
                    m = re.match(r'^(?P<pages>\d+)(?:\D*)$', value.strip())
                    if m:
                        ref_book.pages = int(m.groupdict()['pages'])
                    else:
                        ref_book.pages = 0
                elif '定价' == key:
                    # print('定价: {}'.format(value))
                    m = re.match(r'\d+(?:.\d+)?', value.strip())
                    if None is not m:
                        ref_book.price = float(m[0])
                    else:
                        ref_book.price = float(0.0)
                elif '装帧' == key:
                    ref_book.binding = value
                elif '丛书' == key:
                    ref_book.series = value
                elif 'ISBN' == key:
                    ref_book.isbn13 = value
                else:
                    ok = False

                if not ok:
                    if None is ref_book.debug_memo:
                        ref_book.debug_memo = ''
                    ref_book.debug_memo += '{} => {}\n'.format(key, value)
                    print('[{:>3}] {:>10} => {}'.format(' OK' if ok else 'ERR', key, value))
                    result = False
                pass
        except Exception as ex:
            ex.with_traceback()

            if None is ref_book.debug_memo:
                ref_book.debug_memo = ''
            ref_book.debug_memo += ex

            print('Failed to parse "Other info:, with exception: \n{}"'.format(ex))
            result = False

        return result
