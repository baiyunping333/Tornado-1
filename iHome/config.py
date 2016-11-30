#coding:utf-8

import os

#Application配置参数
settings={
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "template_path": os.path.join(os.path.dirname(__file__),"template"),
    "cookie_secret":"L7+hGgAnRSCxqFso24Pjlbahwr+6s095nOZZ0JGQARg=",
    "xsrf_cookies":True,
    "debug":True,
}

#mysql配置参数
mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="mysql"
)

#redis配置参数
redis_options = dict(
    host="127.0.0.1",
    port=6379
)

log_file = os.path.join(os.path.dirname(__file__),'logs/log.log')
log_level = "debug"

passwd_hash_key="jzHMmyjOSWaZ4sDmocvHRdvbMBebLU/QsySOTyqcfR8="

session_expires = 86400 #session有效期,秒

# http://ohdqvt8kg.bkt.clouddn.com/34f3706addf721d3.gif
image_url_prefix= "http://ohdqvt8kg.bkt.clouddn.com/" #七牛云图片存储域名
