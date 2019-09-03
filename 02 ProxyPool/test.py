# 模块名： test.py
# 用途： 辅助类自定模块，用于爬虫测试


# 函数1： outputHTML
def outputHTML(page, fileName='测试网页', encodeType='utf-8'):
    fileName = '{}.html'.format(fileName)
    with open(fileName, 'w', encoding=encodeType) as fh:
        fh.write(page)
    print('页面已生成...\n')


# 函数2：printDICT
def printDICT(dict):
    for k, v in dict.items():
        print(k, ':', v)


# 函数3：inputString
def inputString(string):
    return string


# 函数4: read
def read(fileName, encodeType='utf-8'):
    with open(fileName, 'r', encoding=encodeType) as fh:
        return fh.read()
