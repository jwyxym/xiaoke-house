from asyncio import run
from aiohttp import ClientSession
from os import makedirs, path
from ssl import create_default_context, CERT_NONE

async def download(url, output_path):
    async with ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content_length = response.headers.get('content-length')
                    if content_length is None:
                        print(f"开始从{url}进行下载")
                    else:
                        print(f"开始从{url}进行下载, 预计字节{getsize(content_length)}")
                    
                    makedirs(path.dirname(output_path), exist_ok=True)
                    
                    with open(output_path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    
                    print(f"下载了{getsize(path.getsize(output_path))}的文件于位置：{output_path}")
                else:
                    print(f"\033[91m从{url}下载失败, 错误代码：{response.status}\033[0m")
        except Exception as e:
            print(f"\033[91m错误：{e}\033[0m")

def getsize(size):
    size = int(size)
    if size is None:
        return '未知字节'
    i = 0
    units = ['B', 'KB', 'MB', 'GB']
    while True:
        if size / 1024 < 1: break
        size /= 1024
        i += 1
    size = str(size)
    if len(size) > 4:
        size = size[: 4]
    return size + units[i]

def start_download(url, output_path):
    run(download(url, output_path))