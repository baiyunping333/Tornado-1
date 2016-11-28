#coding:utf-8
import functools

from utils.response_code import RET

def require_logined(fun):
    @functools.wraps(fun)
    def wrapper(request_handler, *args, **kwargs):
        if request_handler.get_current_user():
            fun(request_handler, *args, **kwargs)
        else:
            request_handler.write(dict(errno=RET.SESSIONERR, errmsg="用户未登陆"))
    return wrapper
