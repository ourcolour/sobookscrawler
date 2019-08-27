#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          sobook_controller.py
@Version:       
@Time:          2019-06-26 14:36
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-26 14:36
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from flask import render_template
from flask import request

from services.sobooks_service import SobooksService

_sobooks_service = SobooksService()


def sobooks_list(page_no=1, page_size=10):
	book_list = _sobooks_service.find(page_no=page_no, page_size=page_size)
	return render_template('/sobooks/list.html', book_list=book_list)


def sobooks_list_ajax(page_size=10):
	# Arguments
	page_no = 1
	if 'page_no' in request.form:
		page_no = int(request.form['page_no'])
	keyword = request.form['keyword'].strip()

	# Query criteria
	filter = {}
	if None is not keyword and len(keyword) > 0:
		filter = {'$or': [
			{'isbn': {'$regex': r'.*' + keyword + '.*'}},
			{'author': {'$regex': r'.*' + keyword + '.*'}},
			{'title': {'$regex': r'.*' + keyword + '.*'}},
		]}
	# {'$text': {'$search': keyword}}

	book_list = _sobooks_service.find(criteria=filter, page_no=page_no, page_size=page_size)

	return render_template('/sobooks/list_item.html', book_list=book_list)


def add_routes(app):
	app.add_url_rule(rule='/sobooks/', view_func=sobooks_list)
	app.add_url_rule(rule='/sobooks/<int:page_no>', view_func=sobooks_list)
	app.add_url_rule(endpoint='list', rule='/sobooks/list/<int:page_no>', view_func=sobooks_list)
	app.add_url_rule(endpoint='list_ajax', rule='/sobooks/list_ajax', methods=['POST'], view_func=sobooks_list_ajax)
