# encoding=utf-8
import requests
import base64
import re
import json
import random
from PIL import Image
from StringIO import StringIO
import rsa
import binascii


# 第一步 调用prelogin.php方法
def get_prelogin():
    global username
    su = base64.urlsafe_b64encode(username)
    pre_data = {"entry": "openapi",
                "callback": "sinaSSOController.preloginCallBack",
                "su": su,
                "rsakt": "mod",
                "checkpin": "1",
                "client": "ssologin.js(v1.4.15)",
                "_": "1461893579134"
                }
    pre_resp = requests.get('https://login.sina.com.cn/sso/prelogin.php', pre_data)
    jsonstr = re.search('{(.*?)}', pre_resp.text).group()
    return json.loads(jsonstr)


# 第二步 获取验证码校验
def get_pin(pre_resp):
    r = random.randint(10000000, 99999999)
    pin_data = {"r": r,
                "s": "0",
                "p": pre_resp['pcid']
                }
    pin_resp = requests.get('https://login.sina.com.cn/cgi/pin.php', pin_data)
    pin_image = Image.open(StringIO(pin_resp.content))
    pin_image.save('d:\\xxx.png')
    checkcode = raw_input("please input checkcode:")
    return checkcode


# 第三步 登录
def post_login(pre_resp):
    global username
    global password
    su = base64.urlsafe_b64encode(username)
    checkcode = get_pin(pre_resp)
    login_data = {"entry": "openapi",
                  "gateway": "1",
                  "from": "",
                  "savestate": "0",
                  "useticket": "1",
                  "pagerefer": "http://toutiao.com/auth/connect/?type=toutiao&platform=sina_weibo",
                  "pcid": pre_resp["pcid"],
                  "ct": "1800",
                  "s": "1",
                  "vsnf": "1",
                  "vsnval": "",
                  "door": checkcode,
                  "appkey": "42iQjj",
                  "su": su,
                  "service": "miniblog",
                  "servertime": pre_resp["servertime"],
                  "nonce": pre_resp["nonce"],
                  "pwencode": "rsa2",
                  "rsakv": pre_resp["rsakv"],
                  "sp": encrypt_password(password, pre_resp),
                  "sr": "1366*768",
                  "encoding": "UTF-8",
                  "cdult": "2",
                  "domain": "weibo.com",
                  "prelt": "256",
                  "returntype": "TEXT"}
    login_resp = requests.get('https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=1461895145060',
                              login_data)
    return login_resp.json()


# 获取加密的密码
def encrypt_password(sp, dict):
    rsa_publickey = int(dict["pubkey"], 16)
    key = rsa.PublicKey(rsa_publickey, 65537)  # 创建公钥
    message = str(dict["servertime"]) + '\t' + str(dict["nonce"]) + '\n' + str(sp)  # 拼接明文js加密文件中得到
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


if __name__ == '__main__':
    username = "18178625545"
    password = "a123456"
    result = post_login(get_prelogin())
    print result
