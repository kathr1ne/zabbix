#!/usr/bin/python
# -*- coding=utf-8 -*-
#

import os
import sys
import time
import json
import requests
import logging
from configparser import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

def get_scripts_path():
    """Full path to location of custom alert scripts"""
    zabbix_serverconf = "/etc/zabbix/zabbix_server.conf"
    with open(zabbix_serverconf, 'r') as f:
        for line in f:
            if line.startswith('AlertScriptsPath'):
                return line.split('=')[-1].strip()

# Log Format
logging.basicConfig(level=logging.INFO,
        format = '%(asctime)s %(filename)s[%(lineno)d]: %(levelname)s %(message)s',
        datefmt = '%F %T',
        filename = '{}.log'.format(os.path.join(get_scripts_path(), os.path.basename(__file__).split('.')[0])),
        filemode = 'w')

# Config
# conf = os.path.join(os.getcwd(), "setting.ini")
conf = os.path.join(get_scripts_path(), "setting.ini")
cfg = ConfigParser()
cfg.read(conf)

def get_times():
    return int(time.time())

class WeChatAlert(object):
    """ We Chat Alert"""
    def __init__(self, cfg):
        self.cfg = cfg

    def get_token(self, corpid, secret):
        """Get token from file or web API"""
        access_token = self.cfg.get('token', 'access_token')
        difft = get_times() - int(self.cfg.get('token', 'expires_time'))
        if difft < 7200:
            token = access_token
            logging.info("use the already obtained token.")
        else:
            tokenurl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            Data = {"corpid": corpid, "corpsecret": secret}
            r = requests.get(url=tokenurl, params=Data)
            if r.json()['errmsg'] == 'ok':
                token = r.json()['access_token']
                logging.info("Re-request token.")
                self.cfg.set('token', 'access_token', token)
                self.cfg.set('token', 'expires_time', str(get_times()))
                with open(conf, 'w') as f:
                    self.cfg.write(f)
            else:
                logging.warning("r.json()['errmsg']")
        return token
    
    def sendmessage(self, *args):
        """send message to wechat users"""
        Corpid = self.cfg.get('auth', 'corpid')
        Secret = self.cfg.get('auth', 'secret')
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(self.get_token(Corpid, Secret))
        wechat_json = {
            "touser": self.cfg.get('target', 'touser'),
            "msgtype": self.cfg.get('target', 'msgtype'),
            "agentid": self.cfg.get('target', 'agentid'),
            "text": {
                "content": "{}\n{}".format(Subject, Content)
            },
            "safe": "0"
        }
        response = requests.post(url, data=json.dumps(wechat_json, ensure_ascii=False, encoding='utf8'))
        if response.json()['errmsg'] == 'ok':
            logging.info("response sendmessage api is ok.")
        else:
            logging.warning(response.json()['errmsg'])

if __name__ == '__main__':
    wechat = WeChatAlert(cfg)
    # 自己决定 touser 是使用zabbix传过来的第一个参数 or 在setting.ini配置文件自定义
    # Touser = sys.argv[1]
    Subject = sys.argv[2]
    Content = sys.argv[3]
    wechat.sendmessage(Subject, Content)
