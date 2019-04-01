import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

urls = [
    'https://api.ipify.org/?format=json',
    'http://pv.sohu.com/cityjson',
    'https://jsonip.com/'
]

def fetch(session,url):
    try:
        with session.get(url,timeout=1) as response:
            pageContent = response.content
            if response.status_code != 200:
                print("连接失败：{0}".format(url))
                print("失败代码: " + response.status_code)
            return pageContent
    except Exception as e:
        print(e)


async def get_data_asynchronous(urls):
    pageContent = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session,url)
                )
                for url in urls
            ]
            for response in await asyncio.gather(*tasks):
                pageContent.append(response)
            return pageContent


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_data_asynchronous(urls))
test = loop.run_until_complete(future)


