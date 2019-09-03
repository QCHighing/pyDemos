import time


class TIME(object):
    """docstring for TIME"""
    def __init__(self, NormalTime=None, UnixTime=None):
        self.__NormalTime = NormalTime      # 字符串
        self.__UnixTime = UnixTime          # 数值
        self.NowUnix = round(time.time())   # 数值

    def unix(self):
        if not self.__UnixTime:
            timeFormat = '%Y-%m-%d %H:%M:%S'
            localTime = time.strptime(self.__NormalTime, timeFormat)
            num = time.mktime(localTime)
            return int(num)
        else:
            return self.__UnixTime

    def normal(self):
        if not self.__NormalTime:
            timeFormat = '%Y-%m-%d %H:%M:%S'
            value = self.__UnixTime
            localTime = time.localtime(value)
            date = time.strftime(timeFormat, localTime)
            return date
        else:
            return self.__NormalTime
