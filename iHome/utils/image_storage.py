# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config
import logging

#需要填写你的 Access Key 和 Secret Key
access_key = '_ZwZuwKYW0cb_5khWr9ji7RgctmPtHA8Uc930y8M'
secret_key = 'SOSg--axDf9d3OC5zRykO-OLcAS5t8BNj_RZTlAg'



#要上传的空间
bucket_name = 'home'

#上传到七牛后保存的文件名
# key = 'my-python-logo.png'
def storage(data):
    """七牛云存储上传文件接口"""
    if not data:
        return None
    try:
        #构建鉴权对象
        q = Auth(access_key, secret_key)
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name)
        ret, info = put_data(token, None, data)
    except Exception as e:
        logging.error(e)
        raise Exception("上传文件到七牛错误")
    if info and info.status_code != 200:
        raise Exception("上传文件到七牛错误")
    return ret["key"]

if __name__ == "__main__":
    file_name = raw_input("Please input the up_file:")
    file =open(file_name, "rb")
    data = file.read()
    print type(data)
    key = storage(data)
    print key
    file.close()
