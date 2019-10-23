_host_format = 'mongodb://{}/{}?replicaSet={}&readPreference={}'
_host_list = [
	('mongo01.dev.xjh.com', 27017),
	('mongo02.dev.xjh.com', 27017),
	('mongo03.dev.xjh.com', 27017),
]
_db_name = 'DoubanBookApi'
_replica_set = 'xjh'
_read_preference = 'nearest'


def _build_connection_string():
	'''
	构造连接字符串
	:return: 连接字符串
	'''
	hosts_string = ''
	for host, port in _host_list:
		cur_host = '{}:{}'.format(host, port)

		if hosts_string:
			hosts_string += ','

		hosts_string += cur_host

	result = _host_format.format(
		hosts_string,
		_db_name,
		_replica_set,
		_read_preference,
	)

	return result


MONGODB_SETTINGS = [
	{
		'host': _build_connection_string(),
	},
	# {
	# 	'host': 'localhost',
	# 	'port': 27018,
	# 	'db': _db_name,
	# },
]
