#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          book_api_controller.py
@Version:       
@Time:          2019-07-01 16:58
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-07-01 16:58
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

from website.controllers.api.base_api_controller import BaseApiController, RESTfulResponse
from website.services.book_service import BookService

_book_service = BookService()


class BookApiController(BaseApiController):

	def get(self, isbn):
		data = _book_service.find_by_isbn(isbn)
		# data = _book_service.find(criteria={'$regex': r'^9787\d+$'})

		response = RESTfulResponse.build_info(data=data)

		return self.build_response(data=response)

	def post(self, id):
		return {'id': id, 'method': 'POST'}
