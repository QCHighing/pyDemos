import os
import requests
from urllib import error


# 下载路径选择
def select_direction(courseName):
    currentDir = os.getcwd()
    currentDir = currentDir.replace("\\", "/") # 美化显示
    path = input(f'>>> 请输入保存路径：(默认在当前路径{currentDir}下创建"{courseName}"文件夹)\n>>> ')  # 获得当前文件夹
    if not path:
        path = currentDir + "/" + courseName
    if not os.path.isdir(path):  # 检测是否是文件夹
        os.mkdir(path)  # 在当前目录下创建文件夹，path = 相对路径
    return path


# 下载文件
def download(url, direction, fileName, fileType, mode="bigfile"):
    # 文件的绝对路径，如 D:\Program Files\Python36\python.exe
    abs_fileName = '{}/{}.{}'.format(direction, fileName, fileType)
    renameCount = 0
    while True:  # 检查是否重名
        if os.path.exists(abs_fileName):
            renameCount += 1
            abs_fileName = '{}/{}-{}.{}'.format(direction, fileName, renameCount, fileType)
        else:
            break
    # 小文件模式：直接下载
    if mode is not 'bigfile':
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(abs_fileName, 'wb') as file:
                file.write(r.content)
        except requests.HTTPError as ex:
            print('[-]ERROR: %s' % ex)
        except KeyboardInterrupt:
            os.remove(abs_fileName)
            raise
        return
    # 大文件模式：分块下载
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        if 'Content-Length' not in r.headers:
            raise requests.HTTPError('No Content Length')
        file_size = int(r.headers['Content-Length'])   # 文件大小：B
        if file_size < 10 * 1024 * 1024:
            chunk_size = 1024 * 1024    # 分块大小 B
        else:
            chunk_size = 3 * 1024 * 1024
        download_size = 0   # 已下载大小：B
        with open(abs_fileName, 'wb') as file:
            for chunk in r.iter_content(chunk_size=chunk_size):
                progress = download_size / file_size * 100  # 下载进度
                prompt_bar = '[{:50}] {:.1f}%\tSize: {:.2f}MB'.format(
                    '=' * int(progress / 2), progress, download_size / 1024 / 1024)
                print(prompt_bar, end='\r')  # \r 代表打印头归位，回到某一行的开头
                file.write(chunk)
                download_size += chunk_size
            print('[{:50}] 100% Done!\tSize: {:.2f}MB'.format('=' * 50, file_size / 1024 / 1024))
    except error.HTTPError as ex:
        print('[-]ERROR: %s' % ex)
    except KeyboardInterrupt:
        os.remove(path)
        raise
