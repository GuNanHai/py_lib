from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

from lxml import etree

#==============================function目录
#               1.scrapeIpProxyList
#               2.getIpProxyList
#               3.getIpList
#===========================================
# 输出：代理ip的列表，每个条目都是一个字典包含ip\port\protocol
def scrapeIpProxyList():
    ipList = []
    url = 'https://free-proxy-list.net/'
    cwd = os.getcwd()

    #通过代理启动测试浏览器
    PROXY = '127.0.0.1'+':8080'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(cwd+'/chromedriver',options=chrome_options)

    driver.get(url)
    driver.implicitly_wait(30)
    locator = (By.LINK_TEXT,'Next')

    while True:
        try:
            WebDriverWait(driver,20,0.5).until(EC.presence_of_all_elements_located(locator))
        except:
            print('进入失败！')
        
        #将网页通过lxml的xpath将数据爬取出来
        selector = etree.HTML(driver.page_source)
        trList =  selector.xpath("//table[@id='proxylisttable']/tbody/tr")
        for each in trList:
            proxy = {}
            temp = each.xpath(".//td[position()=1 or position()=2 or position()=7 ]/text()")
            try:
                proxy['ip'] = temp[0]
                proxy['port'] = temp[1]
                if temp[2]== 'yes':
                    proxy['protocol'] = 'https'
                else:
                    proxy['protocol'] = 'http'
            except:
                continue
            ipList.append(proxy)
        print('Collected %s proxies' % (len(ipList)))
        # 寻找到下一页的按钮，找不到则结束抓取    
        nextPageBtn = driver.find_element_by_link_text('Next')
        if nextPageBtn.value_of_css_property('cursor') == 'not-allowed':
            print('@'*70)
            print(' '*25+'代理IP列表收集完成！')
            print('@'*70)
            break    
        print('尝试进入 %s  ......'%(nextPageBtn.get_attribute('href')))
        nextPageBtn.click()
    driver.quit()
    return ipList

# 输出：生成ip格式为{'https':'https://192.168.1.1:8080'}的字典列表
def getIpProxyList(data):
    ipList = []
    for each in data:
        if each['protocol']=='https':
            ip = {}
            ip['https'] = 'https://'+each['ip']+':'+each['port']
            ipList.append(ip)
    return ipList

# 输出：支持https的代理ip，格式为'192.168.1.1:8080'的列表，可用python脚本proxyPool.py进一步提纯
def getIpList(data):
    ipList = []
    for each in data:
        if each['protocol']=='https':
            
            ip= each['ip']+':'+each['port']
            ipList.append(ip)
    return ipList

def main():
    return getIpList(scrapeIpProxyList());