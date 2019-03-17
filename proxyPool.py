import requests
from lxml import etree
import json
import asyncio
from aiohttp import ClientSession
import aiohttp
import re
#用于将字符串形式的字典对象转化成真正的字典对象
import ast
import random

#================================函数目录
#getIpList()
#async fetch()
#async refineProxies()
#getProxyList()
#getLocalProxies()
#testLocalProxies()


# 从某api提取出指定数量的代理ip，
# 返回：ipList
def getIpList(ipcount):
    ipCount = ipcount
    #此ip接口不能使用代理连接
    api = 'http://www.66ip.cn/mo.php?sxb=&tqsl='+str(ipCount)+'&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D1000%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1'
    response = requests.get(api)
    htmlContent = etree.HTML(response.content)
    rowStringList = htmlContent.xpath('//body/p/text()') 
    ipList = []
    for each in rowStringList:
        temp = each.strip()
        if temp=='':
            continue
        ipList.append(temp)
    return ipList

# 单个异步读取网页的操作
async def fetch(session,url,proxy,header,timeout,count):
    try:
        async with session.get(url,proxy=proxy,headers=header,timeout=timeout) as response:
            pageBytes = await response.read()
            try:
                pageStr = pageBytes.decode('utf-8',errors='ignore')
                dictData = ast.literal_eval(pageStr)
            except Exception as e:
                print('%'*20)
                print(pageBytes)
                print('')
                print(e)
                print('-'*10)
                return None
            print('有效IP： %s' % (dictData))
            ip = dictData['ip']
            # print('网站显示的IP：%s   '%(ip))
            return proxy
    except aiohttp.ClientConnectorSSLError as e:
        print('@'*20+'  SSL Error')
        print(e)
        return None
    except Exception as e:
        # print('*'*20)
        # print(e)
        # print('-'*10)
        return None

# 入口：（ip列表，单个request的超时限制)
# 出口：（有效IP列表)
async def refineProxies(ipList,timeout):
    print('程序将从 %s 个ip中，挑选出有效ip。'  %(len(ipList)))
    url = "https://api.ipify.org/?format=json"
    tasks = []
    userAgents = [ "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    ]
    #使链接申请不检查ssl验证
    connector=aiohttp.TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        for each in ipList:
            count = ipList.index(each) + 1
            proxy = 'http://'+each
            header = { "User:Agent" : random.choice(userAgents)}
            task = asyncio.ensure_future(fetch(session,url,proxy,header,timeout,count))
            tasks.append(task)
        proxyPool = await asyncio.gather(*tasks)
    newProxyPool = []
    for each in proxyPool:
        if each == None:
            continue
        newProxyPool.append(each)
    return newProxyPool

# 输入：想要精炼的ip的数量
# 输出：精炼后的ip列表
# 生成：ip列表文本
def getProxyList(count):
    ipList = getIpList(count)
    loop = asyncio.get_event_loop()
    proxyPool = loop.run_until_complete(refineProxies(ipList,timeout=720))
    print('一共精炼出 %s 个代理IP' % (len(proxyPool)))
    with open('proxyPool.txt','w') as f:
        for each in proxyPool:
            f.write(each+'\n')
    return proxyPool


# 从本地文件中获取不带'http://'【前缀的代理IP列表】
def getLocalProxies():
    with open('proxyPool.txt','r') as f:
        ipList = f.readlines()

    for i in range(len(ipList)):
        ipList[i] = ipList[i].replace('\n','').replace('http://','')
    return ipList
# 测试并打印（代理IP列表）的有效率
def testLocalProxies(ipList):
    loop = asyncio.get_event_loop()
    proxyPool = loop.run_until_complete(refineProxies(ipList,timeout=60))
    
    effectiveRate = len(proxyPool)/len(ipList) * 100
    print('代理池的有效率为：%.1f%% (%s/%s)' % (effectiveRate,len(proxyPool),len(ipList)))

# ipList = getProxyList(10000) 

# def fetchUrls(urls,proxies)