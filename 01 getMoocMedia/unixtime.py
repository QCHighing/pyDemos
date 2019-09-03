import time  # Unix时间戳

# Unix时间戳解码，如string ='1534348800000', number_bits = 13, 毫秒级, 返回值 = '2018/8/16 0:0:0'
def number2time(string, number_bits=13):
    timeFormat = '%Y-%m-%d %H:%M:%S'
    if number_bits is 10:   # 秒级
        value = eval(string) 
    elif number_bits is 13:     # 毫秒级
        value = eval(string) / 1000
    localTime = time.localtime(value)
    date = time.strftime(timeFormat, localTime)
    return date


# 获取当前的Unix时间戳，如获取秒级, number_bits = 10， 返回值 = 1534348800
def now(number_bits=13):
    second = time.time()
    if number_bits is 10:   # 秒级
        return round(second)
    elif number_bits is 13:   # 毫秒级
        millisecond = second * 1000     
        return round(millisecond)
    else:
        return None