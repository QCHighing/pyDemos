import proxypool
import os

proxies = proxypool.get_proxies()
print('获取的代理是：',proxies)
os.system("pause")
