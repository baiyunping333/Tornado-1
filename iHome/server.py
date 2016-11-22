#coding=utf-8

import tornado.web
import tornado.ioloop
import tornado.options
import httpserver
import torndb
import redis

from 

def main():
	app = tornado.web.Application(
    	[(r'/',IndexHandler),
    	]      
    )


if __name__ == "__main__":
	main()