# coding=utf-8

import sys
import json
import base64
import os


from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

from file_path import get_path

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# get youself API_KEY from baidu ai studio
API_KEY = ''

SECRET_KEY = ''


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)

    result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)





if __name__ == '__main__':

    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    

    # 读取书籍页面图片
    image_paths,image_names = get_path('./images', ('.jpg','.png','.jpeg'))
    image_count = len(image_names)
    i = 1
    print('found {} pdf files'.format(image_count))
    for image_path, image_name in zip(image_paths,image_names):
        if not image_path:
            continue
        print('processing {}th file...'.format(i))
        text = ""
        file_content = read_file(image_path)

        # 调用文字识别服务
        result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

        # 解析返回结果
        result_json = json.loads(result)
        for words_result in result_json["words_result"]:
            text = text + words_result["words"]

        # # 保存文本
        text_path = './images/'+image_name+'.txt'
        with open(text_path,'w') as f:
            f.write(text)
        image_count+=1

    print('finished!')
    