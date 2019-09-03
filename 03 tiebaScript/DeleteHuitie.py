#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : DeleteTiebahuitie.py
# @Author   : QCHighing
# @Date     : 2018/06/12 0012 08:06
# @Site     : https://github.com/QCHighing
# @Software : PyCharm

import requests
import re
import test

# 个人账户配置
# 在此处增加账号cookie，以实现自动登录
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


# 爬取我的i贴吧页面，获得当前页的回贴链接列表 huitie_list 和发帖数 huitie_num
def get_huitie_info():
    url = 'http://tieba.baidu.com/i/i/my_reply'
    try:
        page = session.get(url, headers=headers, timeout=30).text
        # test.outputHTML(page, '回贴列表')  # 测试所用
        # 搜索回帖链接 "b_reply" href="/p/5076892780?fid=25008639&amp;pid=120057741369&cid=0&red_tag=1076502146
        re_huitieList = r'"b_reply" href="(/p/\d+\?fid=\d+&[amp;]{0,4}pid=\d+&[amp;]{0,4}cid=[\d#]+)"'
        huitie_list = re.findall(re_huitieList, page)
    except requests.HTTPError as ex:
        print('回贴列表获取失败...\n[-]ERROR: %s' % str(ex))
    return huitie_list


# 提交post请求，删除回贴
def delete_huitie(url):
    try:
        # 访问tbs网页获取tbs，用于post
        url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
        page = session.get(url_tbs).text
        # test.outputHTML(page, 'tbs获取页')
        tbs = re.findall(r'{"tbs":"(.+)","',page)[0]
        # 访问回贴页面，搜索获得其他的post数据
        page = session.get(url, timeout=30).text
        # test.outputHTML(page, '回贴页面')
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
        assert re.search(r'"err_code":0', r.text) != None
        return True
    except:
        return False


def main():
    start_session()
    totle_huitie_num = 0    # 总回贴数
    totle_failed_num = 0    # 总失败数
    totle_delete_num = 0    # 总删贴数
    for i in range(100):
        huitie_list = get_huitie_info()                               # 得到当前页的回贴链接列表
        totle_huitie_num += len(huitie_list) - totle_failed_num       # 得到回贴总数
        if len(huitie_list) > totle_failed_num:
            for item in huitie_list[totle_failed_num:]:
                url = 'https://tieba.baidu.com' + item
                print('正在删除...', url, end='\t\t')
                if delete_huitie(url):
                    totle_delete_num += 1
                    print('删除成功!已删除{:^3}条回贴'.format(totle_delete_num))
                else:
                    totle_failed_num += 1
                    print('删除失败！')
        else:
            break
    print('\n---- 删贴完成!!! ----回贴%d条---- 删除成功%d条 ---- 删除失败%d条 ----' %
        (totle_huitie_num, totle_delete_num, totle_failed_num))


if __name__ == '__main__':
  main()
