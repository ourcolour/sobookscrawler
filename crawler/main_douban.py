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

# Base dir
import os, sys
import click

sys.path.append('/Users/CC/opt/anaconda3/lib/python3.7/site-packages')

from services.job_service import JobService
from services.library_sh_cip_service import LibraryShCipService
from services.capub_cip_service import CapubCipService
from utils import path_util

# Status files
MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg.py')


@click.command()
@click.option('--action', '-a', type=click.Choice(['addtask', 'runtask', 'querycip']))
@click.option('--isbn', type=str,
              default=None)  # '--action', '-a', type=str, type=click.Choice(['fetch', ], default='sobooks'))
@click.option('--limit', type=click.IntRange(1, 50, clamp=True),
              default=10)  # '--action', '-a', type=str, type=click.Choice(['fetch', ], default='sobooks'))
def command_dispatcher(action, isbn, limit):
    with JobService() as cts:
        # Dispatcher
        if 'querycip' == action:
            # Cip querying method,
            # with LibraryShCipService() as svs:
            #     pass
            # A new function for cip info querying
            # added by CC.Yao 2020/05/25
            with LibraryShCipService() as svs:
                isbn_list = []
                if isbn:
                    isbn_list.append(isbn)
                    pass
                for idx, isbn in enumerate(isbn_list):
                    s = svs.get_cip_by_isbn13(isbn13=isbn)
                    print('{} {}'.format(isbn, s))
                pass
            pass
        elif 'addtask' == action:
            isbn_list = isbn.replace(' ', '').split(',')
            for isbn in isbn_list:
                cts.add_task(isbn)
            pass
        elif 'runtask' == action:
            cts.run_task(limit=limit)
            pass
        else:
            print('Invalid `action` value.')


if __name__ == '__main__':
    command_dispatcher()
