#coding:utf-8
from handlers import VerifyCode, Passport, Profile
from tornado.web import StaticFileHandler
import os

handlers = [
    (r'^/api/imagecode$', VerifyCode.ImageCodeHandler),
    (r'^/api/smscode$', VerifyCode.SMSCodeHandler),
    (r'^/api/register$', Passport.RegisterHandler),
    (r'^/api/login$', Passport.LoginHandler),
    (r'^/api/logout$', Passport.LogoutHandler),
    (r'^/api/check_login$', Passport.CheckLoginHandler),
    (r'^/api/profile$', Profile.ProfileHandler),
    (r'^/api/profile/avatar$', Profile.AvatarHandler),

    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))

]
