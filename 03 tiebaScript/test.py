# 模块名： test.py
# 用途： 用于爬虫类测试

from urllib.parse import unquote  # URL文字解码
from bs4 import UnicodeDammit as UD  # 编码检测


# 函数1： outputHTML
def outputHTML(page, fileName='测试网页', encodeType='utf-8'):
    fileName = '{}.html'.format(fileName)
    with open(fileName, 'w', encoding=encodeType) as fh:
        fh.write(page)
    print('页面已生成...\n')


# 函数2：printDICT
def printDICT(dictVar, *varTuple):
    for k, v in dictVar.items():
        print(k, ':', v)
    for item in varTuple:
        print()  # 空行
        printDICT(item)

        
# 函数3：inputString
def inputSTRING(stringVar):
    return stringVar


# 函数4：detect_encoding
def detect_encoding(response):
    detect_result = UD(response.content).original_encoding
    print(detect_result)


# 函数5：printSTRING
def printSTRING(*varTuple):
    for item in varTuple:
        print(item,end=', ')
    print('\n')



