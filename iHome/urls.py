#coding:utf-8
from handlers import VerifyCode

handlers = [
    (r'/',VerifyCode.IndexHandler),
]
