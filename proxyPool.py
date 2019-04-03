import requests
from lxml import etree
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
#用于将字符串形式的字典对象转化成真正的字典对象
import ast
import random
import os
os.environ['no_proxy']='*'

#================================函数目录
#getIpList
#fetch      
#get_data_asynchronous
#refineProxies
#main


# 从某api提取出指定数量的代理ip，
# 返回：ipList
def getIpList(ipcount=300):
    ipCount = ipcount
    #此ip接口不能使用代理连接
    # 下面这个被注释掉的api用于https代理的获取
    # api = 'http://www.66ip.cn/nmtq.php?getnum='+str(ipcount)+'&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'

    api = 'http://www.66ip.cn/mo.php?sxb=&tqsl='+str(ipcount)+'&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D10%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1'
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

def fetch(session,url,headers,proxy,timeout=3):
    try:
        with session.get(url,headers=headers,proxies=proxy,timeout=timeout) as response:
            if response.status_code != 200:
                print("连接失败: {0} ".format(url))
                print("失败代码: " + response.status_code)
                return -1
            print('网站反馈信息：'+response.text)
            return proxy
    except Exception as e:
        return -1

async def get_data_asynchronous(ipList,protocol,timeout=3):
    proxies = []
    responses = []
    # url = 'https://api.ipify.org/?format=json'
    url = 'http://pv.sohu.com/cityjson'
    userAgents = [ "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    ]
    for each in ipList:
        proxies.append({
            protocol:protocol+'://'+each
        })
    with ThreadPoolExecutor(max_workers=100) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session,url,{'User-Agent':random.choice(userAgents)},proxy,timeout)
                )
                for proxy in proxies
            ]
            for response in await asyncio.gather(*tasks):
                responses.append(response)
            return responses

# 输入： 【IP:Port】
def refineProxies(ipList,protocol='http',timeout=3):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(ipList,protocol,timeout))
    responses = loop.run_until_complete(future)
    proxyPool = []
    for each in responses:
        if each==-1:
            continue
        proxyPool.append(each)
    print('代理有效率为： %.2f ' % (len(proxyPool)/len(ipList)))
    with open('proxyPool.json','w') as f:
        json.dump(proxyPool,f)


# 功能，合并多个代理池，
# 输入：json文件名
def merge_proxyPools(*proxyPools):
    finalProxyPool = []
    for each in proxyPools:
        with open(each,'r') as f:
            temp = json.load(f)
            finalProxyPool.extend(temp)
    with open('proxyPool.json','w') as f:
        json.dump(finalProxyPool,f)

# 以下专用于https代理的获取
# def main():
#     refineProxies(getIpList(),'https')

def main():
    refineProxies(getIpList(10000),'http')




# =============================================测试本地代理可用性
# 测试用： 将{'https':'https://192.168.0.1:8080'}的格式转化为【IP:Port】----用于检查本地代理IP池的可用性。
def convert_proxy_format(file='proxyPool.json'):
    with open(file,'r') as f:
        proxyPool = json.load(f)
    newProxyPool = []
    for each in proxyPool:
        if each['http']:
            newProxyPool.append(each['http'].replace('http://',''))
    return newProxyPool

# 开启测试：测试本地代理池可用性。
def startTest():
    refineProxies(convert_proxy_format())











