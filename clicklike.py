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
import time


class browser:
    def __init__(self, username, password):
        self.sessions = requests.Session()
        self.client_id = "1290308714"
        self.appKey = "251ijg"
        self.username = username
        self.password = password

    def run(self):
        login_json = self.post_login(self.get_prelogin())
        self.post_authorize(login_json["ticket"])
        # self.post_authorize("s")

    # 第一步 调用prelogin.php方法
    def get_prelogin(self):
        su = base64.urlsafe_b64encode(self.username)
        timestamp = int(time.time())
        pre_data = {"entry": "openapi",
                    "callback": "sinaSSOController.preloginCallBack",
                    "su": su,
                    "rsakt": "mod",
                    "checkpin": "1",
                    "client": "ssologin.js(v1.4.15)",
                    "_": timestamp
                    }
        pre_resp = requests.get('https://login.sina.com.cn/sso/prelogin.php', pre_data)
        jsonstr = re.search('{(.*?)}', pre_resp.text).group()
        return json.loads(jsonstr)

    # 第二步 获取验证码校验
    def get_pin(self, pre_resp):
        r = random.randint(10000000, 99999999)
        pin_data = {"r": r,
                    "s": "0",
                    "p": pre_resp['pcid']
                    }
        pin_resp = requests.get('https://login.sina.com.cn/cgi/pin.php', pin_data)
        pin_image = Image.open(StringIO(pin_resp.content))
        pin_image.save('/Users/zhangjt/Documents/xxx.png')
        checkcode = raw_input("please input checkcode:")
        return checkcode

    # 第三步 登录
    def post_login(self, pre_resp):
        su = base64.urlsafe_b64encode(self.username)
        checkcode = self.get_pin(pre_resp)
        login_data = {"entry": "openapi",
                      "gateway": "1",
                      "from": "",
                      "savestate": "0",
                      "useticket": "1",
                      "pagerefer": "http://www.yidianzixun.com/",
                      "pcid": pre_resp["pcid"],
                      "ct": "1800",
                      "s": "1",
                      "vsnf": "1",
                      "vsnval": "",
                      "door": checkcode,
                      "appkey": self.appKey,
                      "su": su,
                      "service": "miniblog",
                      "servertime": pre_resp["servertime"],
                      "nonce": pre_resp["nonce"],
                      "pwencode": "rsa2",
                      "rsakv": pre_resp["rsakv"],
                      "sp": self.encrypt_password(self.password, pre_resp),
                      "sr": "1366*768",
                      "encoding": "UTF-8",
                      "cdult": "2",
                      "domain": "weibo.com",
                      "prelt": "256",
                      "returntype": "TEXT"}
        headers = {"Host": "login.sina.com.cn",
                   "User - Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
                   "Referer": "https://api.weibo.com/oauth2/authorize?client_id=1290308714&redirect_uri=http://www.yidianzixun.com/home?page=index-weibo"
                   }
        timestamp = int(time.time())
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=%s' % timestamp
        login_resp = self.sessions.post(url, login_data)
        resp_json = login_resp.json()
        if resp_json["retcode"] <> 0:

            print "login username:%s" % resp_json["nick"]
        return resp_json

    # 授权
    def post_authorize(self, ticket):
        print "ticket%s" % ticket
        redirect_uri = "http://www.yidianzixun.com/home?page=index-weibo"
        reg_callback_url = "https://api.weibo.com/oauth2/authorize?client_id=%s&response_type=code&display=default&redirect_uri=%s" % (
            self.client_id, redirect_uri)
        post_data = {"action": "login",
                     "display": "default",
                     "withOfficalFlag": "0",
                     "quick_auth": "null",
                     "withOfficalAccount": "",
                     "scope": "",
                     "ticket": ticket,
                     "isLoginSina": "",
                     "response_type": "code",
                     "regCallback": reg_callback_url,
                     "redirect_uri": redirect_uri,
                     "client_id": self.client_id,
                     "appkey62": self.appKey,
                     "state": "",
                     "verifyToken": "null",
                     "from": "",
                     "switchLogin": "0",
                     "userId": "",
                     "passwd": ""}
        headers = {"Host": "api.weibo.com",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0",
                   "Referer": "https://api.weibo.com/oauth2/authorize?client_id=1290308714&redirect_uri=http://www.yidianzixun.com/home?page=index-weibo"
                   }
        url = "https://api.weibo.com/oauth2/authorize"
        self.sessions.headers.update(headers)
        resp = self.sessions.post(url, post_data, allow_redirects=False)
        if resp.status_code == 302 or resp.status_code == 301:
            direct_url = resp.headers['Location']
            headers = {"Host": "www.yidianzixun.com",
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0"
                       }
            self.sessions.headers.update(headers)
            resp = self.sessions.get(direct_url)

    # 获取加密的密码
    def encrypt_password(self, sp, dict):
        rsa_publickey = int(dict["pubkey"], 16)
        key = rsa.PublicKey(rsa_publickey, 65537)  # 创建公钥
        message = str(dict["servertime"]) + '\t' + str(dict["nonce"]) + '\n' + str(sp)  # 拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd


if __name__ == '__main__':
    username = "13280499692"
    password = "a123456"
    browser = browser(username, password)
    browser.run()
