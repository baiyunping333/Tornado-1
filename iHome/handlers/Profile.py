#coding:utf-8

from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET

class ProfileHandler(BaseHandler):
    """用户信息"""
    @require_logined
    def get(self):
        name = self.session.data.get("name")
        mobile = self.session.data.get("mobile")
        self.write(dict(errno=RET.OK, errmsg="OK",data={"name":name,"mobile":mobile}))

class AvatarHandler(BaseHandler):
    """头像上传"""
    def post(self):
        pass
