#coding:utf-8
import re
import redis
import torndb

from .BaseHandler import BaseHandler
from utils.response_code import RET

class RegisterHandler(BaseHandler):
    """用户注册"""
    def post(self):
        mobile = self.json_args.get("mobile")
        image_code_text = self.json_args.get("image_code_text")
        sms_code_text = self.json_args.get("sms_code_text")
        password = self.json_args.get("password")
        if not all((mobile, image_code_text, sms_code_text, password)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
        if not match('1\d{10}',mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机号错误"))
        try:
            real_sms_code_text = self.redis.get("sms_code_%s"%mobile)
        except Exception as e:
            return self.write(dict(errno=RET.NODATA, errmsg="短信验证码已过期!"))
        
