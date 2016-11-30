#coding:utf-8
import urllib, urllib2, sys
import json
import logging
host = 'http://api.avatardata.cn/IdCardCertificate/Verify'
method = 'GET'
AppKey = '4c4d6a5eb52f403bbae3a4d44792eb63'

def auth(id_card,real_name):
    #http://api.avatardata.cn/IdCardCertificate/Verify?key=[您申请的APPKEY]&realname=陈龙&idcard=420704198709150033
    # logging.info(type(id_card))
    # logging.info(type(real_name))
    url = host + "?" + "key=" + AppKey + "&realname=" + real_name + "&idcard=" + id_card
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    # print type(response)
    content = response.read()
    content = json.loads(content)
    # logging.info(content)
    error_code = content.get("error_code")
    # logging.info(type(error_code))
    return error_code
    # return response
    # if (content):
    #     print(content)

if __name__ == '__main__':
    k = auth("360111199107076037","徐志伟")
    print k
