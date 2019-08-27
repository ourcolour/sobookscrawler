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
@Time:          2019-06-25 16:56
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019-06-25 16:56
2.  TO-DO
+-------------------------------------------------
'''
from utils import path_util

__author__ = 'cc'

import importlib
import importlib.util
import os
import sys

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from controllers.api.book_api_controller import BookApiController


def _load_controller(app):
	# Module list
	module_list = list()
	# Ignore list
	ignore_file_list = ['__init__.py', '.DS_Store']

	# List all files in `controllers` folder
	root_name = 'controllers'
	root_path = os.path.join(os.path.dirname(sys.argv[0]), root_name)
	for (top, unused_dir_list, file_list) in os.walk(root_path):
		for file in file_list:
			if file in ignore_file_list:
				continue

			top = top.replace(root_path, root_name)
			file = os.path.splitext(file)[0]
			cur_module_path = os.path.join(top, file).replace(os.path.sep, '.')

			module_list.append(cur_module_path)

	# Load module and call `add_routes(app)` function
	for module_path in module_list:
		# Check module existance
		if None is not importlib.util.find_spec(module_path):
			module = importlib.import_module(module_path)
			# Check function existance
			if hasattr(module, 'add_routes'):
				module.add_routes(app)
			else:
				print('{} hasn\'t `add_routes` function'.format(module_path))
				pass


class HomeController(Resource):
	def get(self):
		return {'k': 'v'}


# Status files
# url_for('resources', )

MONGO_CFG_PATH = os.path.join(path_util.get_app_path(), 'resources', 'configs', 'database.cfg')

# Define
db = None
app = None


def run():
	# Path settings
	static_folder = 'resources'
	static_url_path = ''

	# Init flask
	app = Flask(__name__, static_url_path, static_folder)

	# Database
	global db
	db = MongoEngine()
	if os.path.exists(MONGO_CFG_PATH):
		app.config.from_pyfile(MONGO_CFG_PATH)
	db.init_app(app)

	# Add routes - [ Normal Controllers ]
	_load_controller(app)

	# Add routes - [ RESTfuk Controllers ]
	api = Api(app)
	api.add_resource(HomeController, '/')
	api.add_resource(BookApiController, '/v1/book/<string:isbn>')

	# Go running
	app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == '__main__':
	run()
