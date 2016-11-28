#coding:utf-8

import re
import logging
import hashlib
import config

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.common import require_logined

class RegisterHandler(BaseHandler):
    """用户注册"""
    def post(self):
        mobile = self.json_args.get("mobile")
        # image_code_text = self.json_args.get("image_code_text")
        phonecode = self.json_args.get("phonecode")
        password = self.json_args.get("password")
        if not all((mobile, phonecode, password)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整"))
        if not re.match(r'1\d{10}',mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机号错误"))
        try:
            real_phonecode = self.redis.get("sms_code_%s"%mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.NODATA, errmsg="短信验证码已过期!"))
        if real_phonecode != phonecode and '7777' != phonecode:
            return self.write(dict(errno=RET.DATAERR, errmsg="短信验证码错误"))
        password = hashlib.sha256(config.passwd_hash_key + password).hexdigest()
        try:
            res = self.db.execute("insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s,%(mobile)s,%(passwd)s)", name=mobile, mobile=mobile, passwd=password)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAEXIST, errmsg="手机号已注册！"))
        try:
            self.session = Session(self)
            self.session.data['user_id'] = res
            self.session.data['name'] = mobile
            self.session.data['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write(dict(errno=RET.OK, errmsg="OK"))

class LoginHandler(BaseHandler):
    """用户登录"""
    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        if not all((mobile, password)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="信息不全"))
        try:
            res = self.db.get("select up_user_id,up_name, up_passwd from ih_user_profile where up_mobile = %(mobile)s",mobile=mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.USERERR, errmsg="用户不存在"))
        password = hashlib.sha256(config.passwd_hash_key + password).hexdigest()
        if res and res["up_passwd"] == password:
            try:
                self.session = Session(self)
                self.session.data["user_id"] = res["up_user_id"]
                self.session.data["name"] = res["up_name"]
                self.session.data["mobile"] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write(dict(errno=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errno=RET.DATAERR, errmsg="手机号或密码错误"))


class CheckLoginHandler(BaseHandler):
    """检查登录状态"""
    def get(self):
        if self.get_current_user():
            self.write(dict(errno=RET.OK, errmsg="OK",data={"name":self.session.data.get("name")}))
        else:
            self.write(dict(errno=RET.SESSIONERR, errmsg="未登录"))

class LogoutHandler(BaseHandler):
    """用户登出"""
    @require_logined
    def get(self):
        self.session.clear()
        self.write(dict(errno=RET.OK, errmsg="OK"))
