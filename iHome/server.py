#coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import redis
import torndb
import config

from tornado.web import Application, RequestHandler
from tornado.options import options, define
from urls import handlers


define('port', type=int, default=8000, help="指定服务器端口")

class Application(tornado.web.Application):
	"""重写Application类，增加数据库"""
	def __init__(self, *args, **kwargs):
		super(Application,self).__init__(*args, **kwargs)
		self.db = torndb.Connection(**config.mysql_options)
		self.redis = redis.StrictRedis(**config.redis_options)

def main():
	options.logging = config.log_level
	options.log_file_prefix = config.log_file
	tornado.options.parse_command_line()
	app = Application(
			handlers, **config.settings
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
	main()
