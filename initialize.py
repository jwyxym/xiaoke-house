from os import makedirs, path
from json import load, dump
import example

def create_folder(folder_path):
    if not path.exists(folder_path):
        try:
            makedirs(folder_path)
            print(f"成功创建文件夹：'{folder_path}'")
            return True
        except OSError as error:
            if error.errno == errno.EEXIST:
                print(f"文件夹：'{folder_path}'已存在")
                return True
            else:
                print("\033[91m错误：创建文件夹失败\033[0m")
                return False
    return True

def create_file(file_path):
    if not path.exists(file_path):
        try:
            with open(file_path, 'w') as f:
                dump(example.data, f, indent=4)
            print(f"成功创建文件：'{file_path}'")
            return True
        except OSError as e:
            print(f"\033[91m写入文件错误：{e}\033[0m")
            return False
        except Exception as e:
            print(f"\033[91m错误：{e}\033[0m")
            return False
    return True

def proxy_url(json, url):
    proxy = ''
    if url[: 19] == 'https://github.com/':
        proxy = json['proxy']['github']
    return proxy + url

def get():
    if create_file('download.json'):
        with open('download.json', 'r', encoding='utf-8') as file:
            download = load(file)
        url = download['url']
        folder_path = download['folder_path']
        output_name = download['output_name']
        output_type = download['output_type']
        forbidden_name = download['forbidden_name']
        extra_number = ''

        if (url is None or url == '') and download['mode'] == 0:
            while url is None or url == '':
                url = input('请输入下载地址：')
        elif download['mode'] == 1:
            print(f"\033[91m错误:缺少下载地址\033[0m")
            return False, 0, 0, 0

        url = proxy_url(download, url)

        if output_name is None or output_name == '':
            slashes = url.rfind('/')
            if slashes != -1:
                output_name  = url[slashes + 1 :]
                dot = output_name.find('.')
                if dot != -1:
                    output_name = url[slashes + 1 : slashes + dot + 1]
                    if output_type is None or output_type == '':
                        output_type = url[slashes + dot + 1 :]
        elif output_type is None or output_type == '':
            dot = url.rfind('.')
            if dot != -1:
                output_type = url[dot :]
        
        while output_name is None or output_name == '':
            output_name = input('请输入文件名：')
            
        if output_type is None or output_type == '':
            output_type = input('请输入文件后缀：')

        if output_type and output_type[: 1] != '.':
            output_type = f".{output_type}"
        
        for char in forbidden_name:
            output_name = output_name.replace(char, "")

        if len(output_type) + len(output_name) + len(folder_path) >= 230:
            output_name = output_name[: 230 - len(output_name) - len(folder_path) - 10]

        output_path = folder_path + '/' + output_name + extra_number + output_type
        e = 1
        while path.exists(output_path):
            extra_number = f"({e})"
            e += 1
            output_path = folder_path + '/' + output_name + extra_number + output_type

        return True, url, output_path, folder_path
    return False, 0, 0, 0
