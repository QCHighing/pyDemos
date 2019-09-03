#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : DeleteTiebaFatie.py
# @Author   : QCHighing
# @Date     : 2018/06/12 0012 08:06
# @Site     : https://github.com/QCHighing
# @Software : PyCharm

import requests
import re
import test

# 个人账户配置
# 在此处增加账号cookie和百度ID，以实现自动登录
cookie = ''
user_name = ''  # 如张三

# 全局变量声明
global headers
global session
data = {'ie': 'utf-8',
        'tbs': '',
        'kw': '',
        'fid': '',
        'tid': '',
        'user_name': '',
        'delete_my_post': '1',
        'delete_my_thread': '0',
        'is_vipdel': '1',
        'pid': '',
        'is_finf': 'false'}

# 会话设置：定义抓包所得的headers，将cookie导入会话，以保持登录
def start_session():
  global headers, session
  headers = {'Host': 'tieba.baidu.com',
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
             'Accept-Encoding': 'gzip,deflate',
             'Referer': '',
             'Cookie': cookie,
             'DNT': '1',
             'Upgrade-Insecure-Requests': '1',
             'Cache-Control': 'max-age=0',
             'Connection': 'keep-alive',
             }
  cookie_dict = {'Cookie': cookie}
  cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
  session = requests.session()
  session.cookies = cookies


# 爬取我的i贴吧页面，获得当前页的发贴链接列表 fatie_list 和发帖数 fatie_num
def get_fatie_info():
    url = 'http://tieba.baidu.com/i/i/my_tie'
    try:
        page = session.get(url, headers=headers, timeout=30).text
        # test.outputHTML(page, '发贴列表')  # 测试所用
        # 搜索回帖链接 <a href="/p/5753143164?pid=120354517001&amp;cid=0#120354517001"
        re_fatieList = r'<a href="(/p/\d+\?pid=\d+&amp;cid=[#\d]+)"'
        fatie_list = re.findall(re_fatieList, page)
    except requests.HTTPError as ex:
        print('发贴列表获取失败...\n[-]ERROR: %s' % str(ex))
    return fatie_list


# 提交post请求，删除发贴
def delete_fatie(url):
    try:
        # 访问tbs网页获取tbs，用于post
        url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
        page = session.get(url_tbs).text
        # test.outputHTML(page, 'tbs获取页')
        tbs = re.findall(r'{"tbs":"(.+)","',page)[0]
        # 搜索获得其他的post数据
        page = session.get(url, timeout=30).text
        # test.outputHTML(page, '发贴页面')
        data['kw'] = re.findall(r'kw:\'(.{2,8})\',', page)[0]
        data['fid'] = re.findall(r'fid:\'(\d+)\'', page)[0]
        data['tid'] = re.findall(r'tid:\'(\d+)\'', page)[0]
        data['pid'] = re.findall(r'pid=(\d+)', page)[0]
        data['user_name'] = user_name
        data['tbs'] = tbs
        # test.printDICT(data) # 测试所用
        # post删帖，并重新访问已删帖子，确认删除成功
        r = session.post('http://tieba.baidu.com/f/commit/post/delete', data=data)
        # print(r.status_code, r.text)
        page = session.get(url).text
        # test.outputHTML(page,'删除界面')
        assert re.search(r'很抱歉，您的贴子已被自己删除', page) != None
        return True
    except:
        return False



def main():
    start_session()
    totle_fatie_num = 0     # 总发贴数
    totle_failed_num = 0    # 总失败数
    totle_delete_num = 0    # 总删贴数
    for i in range(100):
        fatie_list = get_fatie_info()                               # 得到当前页的发贴链接列表
        totle_fatie_num += len(fatie_list) - totle_failed_num       # 得到发贴总数
        if len(fatie_list) > totle_failed_num:
            for item in fatie_list[totle_failed_num:]:
                url = 'https://tieba.baidu.com' + item
                print('正在删除...', url, end='\t\t')
                if delete_fatie(url):
                    totle_delete_num += 1
                    print('删除成功!已删除{:^3}条发贴'.format(totle_delete_num))
                else:
                    totle_failed_num += 1
        else:
            break
    print('\n---- 删贴完成!!! ----发贴%d条---- 删除成功%d条 ---- 删除失败%d条 ----' %
        (totle_fatie_num, totle_delete_num, totle_failed_num))


if __name__ == '__main__':
  main()
