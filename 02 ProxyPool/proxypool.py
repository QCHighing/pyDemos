import requests
import socket
import re
import sql
import test
from unix import TIME


def get_webpage():
    url = 'http://www.xicidaili.com/'
    headers = {'Accept': 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*',
               'Accept-Language': 'zh-CN',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
               'UA-CPU': 'AMD64',
               'Accept-Encoding': 'gzip, deflate',
               'Host': 'www.xicidaili.com',
               'Connection': 'keep-alive',
               }
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        page = r.text
        # test.outputHTML(page, '西刺代理')  # 生成本地文件，用于测试
        return page
    except:
        time.sleep(15)      # 休息15秒
        get_webpage()


def parse_page(page):
    re_ulist = r'<td>([\d\.]+)</td>\W*?'    \
               r'<td>(\d+)</td>\W*?'        \
               r'<td>(.*)</td>\W*?'         \
               r'<td class="country">(.*)</td>\W*?' \
               r'<td>(.*)</td>'
    # [118.190.95.35] [9001] [广西] [高匿] [HTTP]
    ulist = re.findall(re_ulist, page)
    for item in ulist:
        yield item


def fill_proxypool():
    page = get_webpage()  # 爬取西刺代理网站，注意频度保持在15分钟以上
    # page = test.read('西刺代理.html', 'utf-8') # 测试所用，读取本地网页，避免频繁爬取被封杀
    counter = 1
    for item in parse_page(page):
        print('正在更新：{0:^2} - {1:<16}'.format(counter, item[0]), end='\t')
        if sql.insert(item[0], item[1], item[2], item[3], item[4]):
            counter += 1
        else:
            print('重复插入')
    sql.commit()
    print('\n此次共更新 %d 条代理IP\n' % (counter - 1))


def query_ip_other(ip):
    url = "http://www.ip-api.com/json/" + ip
    try:
        r = requests.get(url)
        r.raise_for_status()
        i = r.json()['data']
        country = i['country']  # 国家
        city = i['city']  # 城市
        isp = i['isp']  # 运营商
        print(u'国家: %s\n城市: %s\n运营商: %s\n' % (country, city, isp))
    except Exception as e:
        # ip = proxies.get('http', None)
        print(f"备用方案依旧出错")
        return None


def query_ip(proxies=None, ip=None):
    # 百度的IP查询功能挂掉了，用Taobao的吧
    # url = 'http://www.baidu.com/s?wd=ip'
    # if proxies:
    #     print('\n测试IP：', end='\t')
    #     r = requests.get(url, proxies=proxies, timeout=5)
    # else:
    #     print('本机IP：', end='\t')
    #     r = requests.get(url, timeout=10)
    if proxies:
        print('\n正在查询代理IP...', end='\n')
    else:
        print('正在查询本机IP...', end='\n')
        myname = socket.getfqdn(socket.gethostname())
        ip = socket.gethostbyname(myname)
        print(f"本机IP： {ip}")
        return ip   # 如需查询本机IP的具体信息，则注释该行
    try:
        r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
        r.raise_for_status()
        i = r.json()['data']
        country = i['country']  # 国家
        area = i['area']  # 区域
        region = i['region']  # 地区
        city = i['city']  # 城市
        isp = i['isp']  # 运营商
        print(u'国家: %s\n区域: %s\n省份: %s\n城市: %s\n运营商: %s\n' % (country, area, region, city, isp))
    except Exception as e:
        # ip = proxies.get('http', None)
        print(f"淘宝IP查询出错，请调试")
        print(e, "\n正在更换备用方案..\n")
        ip = query_ip_other(ip)
    return ip


def select_proxy():
    myIP = query_ip()
    if myIP == None:
        raise Exception('本机IP获取失败！')
    while True:
        ip_info = sql.get()
        if not ip_info:
            raise Exception('代理获取失败，请更新代理池')
        proxies = {'http': '{}:{}'.format(ip_info[0], ip_info[1])}
        # print(f"proxies={proxies}")  # proxies={'http': '60.13.42.87:9999'}
        xIP = query_ip(proxies, ip=ip_info[0])  # 查询代理IP
        if xIP == None or xIP == myIP:
            sql.update(ip_info[0], 'STATUS', '失效')
            print('无效代理 或 IP查询失败，继续测试下一条IP\n')
        else:
            sql.update(ip_info[0], 'STATUS', '有效代理')
            print('测试通过！\n')
            return proxies


def get_proxies():
    curTime = TIME(UnixTime=TIME().NowUnix)  # 获得当前时间
    sql.start()
    if sql.insert(ip='000.000.0.000', port='8888', addr='爬取时间', time=curTime.normal()):
        fill_proxypool()  # 第一次爬取代理网站
    else:
        time_info = sql.get(ip='000.000.0.000')[6]
        lastTime = TIME(NormalTime=time_info)
        diffTime = (curTime.unix() - lastTime.unix()) / 60  # 相差多少分钟
        # 距上次爬取超过30分钟，则更新代理池
        if diffTime > 30:
            print('代理池需要更新，请稍后...')
            fill_proxypool()
            sql.update('000.000.0.000', 'TIME', curTime.normal())
        else:
            print('代理池无需更新')
    proxy = select_proxy()
    sql.close()
    return proxy
