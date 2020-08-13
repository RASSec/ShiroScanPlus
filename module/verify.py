#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import random
import requests
import string

from module.scripts import scripts


def verify(url, dnslog_url='{randstr}',
           check_dnslog_url='{randstr}',
           dns_log_flag='', mode='fast'):
    # 增加可选的验证功能，使用DNSLog验证，方便批量验证。
    randstr = ''.join(random.sample(string.ascii_letters, 8))
    if '{randstr}' in check_dnslog_url:
        check_dnslog_url = check_dnslog_url.format(randstr=randstr)
    if '{randstr}' in dnslog_url:
        dnslog_url = dnslog_url.format(randstr=randstr)
    dnslog_command = "ping {dnslog_url}".format(dnslog_url=dnslog_url)
    scripts(url, dnslog_command, mode)
    print('DNSLOG: {}'.format(dnslog_url))
    print('CHECK DNSlog: {}'.format(check_dnslog_url))
    try:
        resp = requests.get(check_dnslog_url)
        if dns_log_flag in resp.text:
            return True
        return False
    except Exception as err:
        print(err)
        return False
