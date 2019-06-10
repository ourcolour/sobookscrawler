#!/usr/bin/env python 
#  -*- coding: utf-8 -*-

'''
+-------------------------------------------------
@Author:        cc
@Contact:       yaochen@xjh.com
@Site:          http://www.xjh.com
@Project:       sobookscrawler
@File:          ebook_service.py
@Version:       
@Time:          2019/5/30 16:52
@Description:   TO-DO
+-------------------------------------------------
@Change Activity:
1.  Created at  2019/5/30 16:52
2.  TO-DO
+-------------------------------------------------
'''
__author__ = 'cc'

import ebooklib
import ebooklib.epub
import html2text
import jieba


class EBookService(object):

	def read(self, file_path):
		doc = {}

		book = ebooklib.epub.read_epub(file_path)

		h = html2text.HTML2Text()
		h.ignore_link = True

		for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
			html = item.content.decode('utf-8')
			txt = h.handle(html)

			txt = jieba.cut(txt)
			txt = ' '.join(txt)

			print(txt)

		print(txt)

		return

		jieba.cut('Fest')


NOT_ALLOW = ['r', 'm', 'q', 'd', 'p', 'c', 'u', 'e', 'y', 'o', 'h', 'k', 'w', 'x', 'u']


def is_valid_word(word, flag=None):
	result = True

	if None is word or len(word) < 1:
		result = False
	elif None is not flag:
		cap = flag.lower()
		if cap in NOT_ALLOW:
			result = False

	return result


def task(file_path):
	from pyspark.sql import SparkSession

	session = SparkSession.builder.master('local[*]').getOrCreate()
	text_file = session.read.text(file_path)

	text_file.foreach(
		lambda row:
		print('{} -> {}'.format('V', row.Value))
	)

	return True


def main():
	file_path = '/Volumes/Data/Calibre 书库/Liu Yan Gang/Luo Ma Di Guo De Meng Yan _Ma Sai Li Nu Si Bi Xia De Dong Fang Zhan Zheng Yu Dong Fang Man Zu (7656)/Luo Ma Di Guo De Meng Yan _Ma Sai Li Nu Si - Liu Yan Gang.epub'
	file_path = '/Users/cc/Desktop/txt/没有名字的人.txt'

	result = task(file_path)

	print('-' * 10)
	print('RESULT: {}'.format(result))
	print('-' * 10)


#
# with open(file_path, 'r') as f:
# 	lines = f.readlines()
#
# 	cur_line = 0
# 	total_line = len(lines)
#
# 	for idx in range(0, total_line):
# 		line = lines[idx].strip()
#
# 		if not is_valid_word(line):
# 			continue
#
# 		words = pseg.cut(line)
# 		for word, flag in words:
# 			if not is_valid_word(word, flag):
# 				continue
#
# 			print('%s %s' % (word, flag))
#
# 			if idx >= 10:
# 				break


if __name__ == '__main__':
	main()
