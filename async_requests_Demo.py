import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
# =================================Async Requests===============================================
# 需要修改的fetch函数
def fetchCoverImg(session,novel):
    if novel['novel_cover_img_link']:
        url = novel['novel_cover_img_link']
    else:
        return 0
    headers = {'User-Agent':random.choice(userAgents)}
    proxies = random.choice(proxyPool)
    imgPath = novel_sources_dir + '/' + str(novel['novel_id']) + '/' + novel['novel_cover_img_name']
    try:
        with session.get(url,headers=headers,proxies=proxies,timeout=5) as response:
            if response.status_code != 200:
                print("连接失败：{0}".format(url))
                print("失败代码: " + response.status_code)
                #失败获取目录页面，则返回目录页面的str类型url，用于下一轮连接请求。
                return novel
            # 如果发现网页不是图片则不下载
            if response.text.find('html')!=-1:
                print('pass')
                return 0

            pageContent = response.content
            with open(imgPath,'wb') as f:
                f.write(pageContent)
            print('id: %s 小说名：【 %s 】的封面图片下载成功！'%(novel['novel_id'],novel['novel_name']))
            return 0
    except Exception as e:
        print(e)
        return novel
# 异步操作的模板容器，只需替换掉fetchCoverImg方法
async def asyncContainer(dicts_list,fetchFun):
    connectionFailedObj = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetchFun,
                    *(session,dictObj)
                )
                for dictObj in dicts_list
            ]
            for response in await asyncio.gather(*tasks):
                if response:
                    #获取失败的链接所属的字典对象
                    connectionFailedObj.append(response)
            return connectionFailedObj

# 启动异步操作
def startAsyncRequests(dicts_list,fetchFun):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(asyncContainer(dicts_list,fetchFun))
    connectionFailedObj = loop.run_until_complete(future)
    if connectionFailedObj:
        startAsyncRequests(connectionFailedObj)

