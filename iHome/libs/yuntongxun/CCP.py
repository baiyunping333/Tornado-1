#coding=utf-8

from CCPRestSDK import REST
import ConfigParser

#主帐号
_accountSid= '8a216da8588b296f01588b71d5cc00a9'
#说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID。

#主帐号Token
_accountToken= 'f7cd294ffef74c74bd7b2a41a0ad7c3e'
#说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN。

#应用Id
_appId='8a216da8588b296f01588b71d75200b0'
#请使用管理控制台首页的APPID或自己创建应用的APPID.

#请求地址，格式如下，不需要写http://
_serverIP='sandboxapp.cloopen.com'
#说明：请求地址，生产环境配置成app.cloopen.com。

#请求端口
_serverPort='8883'
#说明：请求端口 ，生产环境为8883.

#REST版本号
_softVersion='2013-12-26'
 #说明：REST API版本号保持不变。

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

class _CCP(object):
    def __init__(self):
        #初始化REST SDK
        self.rest = REST(_serverIP, _serverPort, _softVersion)
        self.rest.setAccount(_accountSid, _accountToken)
        self.rest.setAppId(_appId)

    # 生成单例类
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        return self.rest.sendTemplateSMS(to, datas, tempId)

#调用单例类
ccp = _CCP.instance()

if __name__  == "__main__":
    ccp.sendTemplateSMS("18736008450", ['1234',5], 1)
