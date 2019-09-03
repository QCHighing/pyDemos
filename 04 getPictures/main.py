import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver      
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # 等待条件


browser = None

def browserStart():
    global browser
    print('正在无窗启动FireFox浏览器...', end='\t')
    options = webdriver.firefox.options.Options()
    options.add_argument('-headless')                          # 设置无头参数
    browser = webdriver.Firefox(options=options)               # 无界面启动浏览器
    print('启动成功！')


def get_HomePage(url): 
    print('\n正在爬取首页，请稍后...',end='\t')
    browser.get(url)                                           # 打开网页，网页框架加载完成即返回，未加载额外的Ajax请求等
    wait = WebDriverWait(browser, 10)                          # 等待节点完全加载出来，设置最大等待时长10秒
    wait.until(EC.element_to_be_clickable((By.ID, 'submit')))  # 显式等待id='submit'可点击，加载失败则抛出异常
    page = browser.page_source                                 # 获取页面代码
    print('爬取成功！')
    return page


def get_NextPage(pageIndex):
    print('\n正在爬取第%d页，请稍后...' % pageIndex,end='\t')
    browser.find_element_by_link_text("下一页").click()         # 点击“下一页”
    wait = WebDriverWait(browser, 10)                          # 等待节点完全加载出来，设置最大等待时长10秒
    wait.until(EC.element_to_be_clickable((By.ID, 'submit')))  # 显式等待id='submit'可点击，加载失败则抛出异常
    page = browser.page_source                                 # 获取页面代码
    print('爬取成功！')
    return page


def browserClose():
    browser.close()                                            # 关闭浏览器
    print('\n无窗浏览器已关闭')


def download(URL,Path,Name,Type='jpg'):
    if not os.path.isdir(Path):     # 检测文件夹是否存在
        os.mkdir(Path)              # 在当前目录下创建文件夹
    fullName = '%s/%s.%s' % (Path,Name,Type)
    renameCount = 0
    while True:  # 重名处理
        if os.path.exists(fullName):
            print('已跳过')
            return      # 注释该行则同时保存重名文件，打开注释则跳过已下载项
            renameCount += 1
            fullName = '%s/%s-%d.%s' % (Path,Name,renameCount,Type)
        else:
            break
    for i in range(3):      # 设置最大下载失败次数为3
        try:
            r = requests.get(URL)
            r.raise_for_status()
            with open(fullName, 'wb') as file:
                file.write(r.content)
            print('下载成功')
            break
        except:
            continue
    else:
        print('下载失败')


def parseWeb(page, pageIndex):
    folder = '第%02d页' % pageIndex
    soup = BeautifulSoup(page, 'lxml')
    taglist = soup.select('ol li')  # 选出ol标签中所有的li标签
    for li in taglist:
        try:
            pic_name = li.attrs['id'][8:]       # 3871293
            pic_tags = li.find('img')           # type = 'bs4.element.Tag'
            pic_urls = pic_tags.attrs['src']    # type = 'str'
            pic_type = 'jpg' if re.search(r'\.jpg',pic_urls) else 'gif'
            print('正在下载：  {:<70}'.format(pic_urls), end='\t')
            download(pic_urls, folder, pic_name, pic_type)
        except:
            # 跳过广告和无关项
            continue


def main():
    page_num = 1
    browserStart()
    url = 'http://jandan.net/ooxx'
    page = get_HomePage(url)
    for pageIndex in range(1,page_num+1):
        parseWeb(page, pageIndex)
        if pageIndex < page_num:
            page = get_NextPage(pageIndex+1)
    browserClose()


if __name__ == '__main__':
    main()

