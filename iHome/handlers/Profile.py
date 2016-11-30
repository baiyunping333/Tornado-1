#coding:utf-8
import logging
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET
from config import image_url_prefix
from utils.image_storage import storage
from libs.auth.auth import auth
class ProfileHandler(BaseHandler):
    """用户信息"""
    @require_logined
    def get(self):
        # name = self.session.data.get("name")
        # mobile = self.session.data.get("mobile")
        user_id = self.session.data.get("user_id")
        try:
            res = self.db.get("select up_avatar,up_name, up_mobile from ih_user_profile where up_user_id = %s",user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="数据库查询出错"))
        if res.up_avatar:
            avatar_url = image_url_prefix + res.up_avatar
        else:
            avatar_url = ""
        data = {
            "name":res.up_name,
            "mobile":res.up_mobile,
            "avatar_url":avatar_url
        }
        self.write(dict(errno=RET.OK, errmsg="OK",data=data))

class AvatarHandler(BaseHandler):
    """头像上传"""
    @require_logined
    def post(self):
        user_id = self.session.data.get("user_id")
        try:
            pic_data = self.request.files.get("avatar")[0].body
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.PAEAMERR, errmsg="参数错误"))
        try:
            pic_name = storage(pic_data)
        except Exception as e:
            logging.error(e)
            pic_name = None
        if not pic_name:
            return self.write(dict(errno=RET.THIRDERR, errmsg="七牛保存失败"))
        try:
            ret = self.db.execute("update ih_user_profile set up_avatar = %s where up_user_id = %s",pic_name,user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="数据库存储失败"))
        # pic_url = config.image_url_prefix + "/" + pic_name + ".jpg"
        pic_url = image_url_prefix + pic_name
        self.write(dict(errno=RET.OK, errmsg="OK",data={"pic_url":pic_url,"user_id":user_id}))

class NameHandler(BaseHandler):
    """用户名修改"""
    @require_logined
    def post(self):
        username = self.json_args.get("name")
        try:
            user_id = self.session.data.get("user_id")
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.SESSIONERR, errmsg="用户未登录"))
        if username in (None, ""):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不能为空"))
        try:
            ret = self.db.execute("update ih_user_profile set up_name = %s where up_user_id = %s",username,user_id)
        except Exception as e:
            logging(e)
            return self.write(dict(errno=RET.DBERR, errmsg="数据更新失败"))
        try:
            self.session.data["name"] = username
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write(dict(errno=RET.OK, errmsg="OK"))

class AuthHandler(BaseHandler):
    """实名认证"""

    @require_logined
    def get(self):
        """获取认证信息"""
        try:
            user_id = self.session.data.get("user_id")
        except Exception as e:
            logging.error(e)
            self.write(dict(errno=RET.SESSIONERR, errmsg="用户未登录"))
        try:
            ret = self.db.get("select up_real_name, up_id_card from ih_user_profile where up_user_id = %s",user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="数据库查询错误"))
        if not ret:
            return self.write(dict(errno=RET.NODATA, errmsg="该用户未进行实名认证"))
        data = {
            "real_name" : ret.get("up_real_name",""),
            "id_card" : ret.get("up_id_card", "")
        }
        self.write(dict(errno=RET.OK, errmsg="OK", data=data))

    @require_logined
    def post(self):
        """提交认证信息"""
        user_id = self.session.data.get("user_id")
        real_name = self.json_args.get("real_name")
        id_card = self.json_args.get("id_card")
        if real_name in (None,"") and id_card in (None, ""):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
        try:
            id_card = id_card.encode("utf-8")
            real_name = real_name.encode("utf-8")
            # logging.info(type(id_card))
            # logging.info(type(real_name))
            error_code = auth(id_card, real_name)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg="阿凡达请求出错"))
        if 1 == error_code:
            return self.write(dict(errno=RET.DATAERR, errmsg="身份证号不匹配"))
        elif 0 == error_code:
            try:
                ret = self.db.execute("update ih_user_profile set up_real_name = %s,up_id_card = %s where up_user_id = %s",real_name,id_card,user_id)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DBERR, errmsg="数据存储失败"))
            self.write(dict(errno=RET.OK, errmsg="OK"))
