'''
AES有三种密钥长度16(*AES-128*), 24 (*AES-192*), 和 32 (*AES-256*)
在对字符进行加密时，密码和明文长度必须为16,24,或32
因此要对密码和明文进行预处理，确保密码长度为16,24或32，明文长度为16,24或32的整数倍
这里以16(*AES-128*)，ECB模式为例
密钥长度16，明文长度为16的整数倍，若不足则补齐
'''
from Crypto.Cipher import AES
from binascii import unhexlify,hexlify


# 按字节数补齐，输入字符串，返回字节类型
def align(string, isKey=False):
    b_string = string.encode()
    length = len(b_string)
    # 如果接收的字符串是密钥，且长度超16，则截取后返回
    if isKey and length > 16:
        return b_string[0:16]
    # 缺位需补齐
    if length % 16:
        addcnt = 16 - length % 16
        b_string += '\000'.encode() * addcnt
    return b_string


# ECB模式加密
def enc(key,src_text):                  # 源文本：你好，明天
    key = align(key,True)                    
    ecd_text = align(src_text)          # 将源文本编码并对齐，encode
    obj = AES.new(key,AES.MODE_ECB)     # 实例化加密对象
    ecr_text = obj.encrypt(ecd_text)    # 加密，encrypt，有乱码：   b'\x8ed2\xda\xf3\x9a\'"\xfe\xf8\x083JC\x8bG'
    hex_text = hexlify(ecr_text)        # 转为十六进制字节类型： b'8e6432daf39a2722fef808334a438b47'
    text = hex_text.decode()            # 解码，得到字符串：  8e6432daf39a2722fef808334a438b47
    return text                         


def dec(key,text):                      # 加密处理后的字符串：8e6432daf39a2722fef808334a438b47
    key = align(key,True)                    
    hex_text = text.encode()            # 编码，得到字节型：b'85b087ddb6d3dbf68ba08ef6cd21c715'
    str_text = unhexlify(hex_text)      # 转为字节编码： b'\x85\xb0\x87\xdd\xb6\xd3\xdb\xf6\x8b\xa0\x8e\xf6\xcd!\xc7\x15'
    obj = AES.new(key,AES.MODE_ECB)     # 实例化解密对象
    dec_text = obj.decrypt(str_text)    # 解密，得到源文本的字节流： b'\xe4\xbd\xa0\xe5\xa5\xbd\xef\xbc\x8c\xe6\x98\x8e\xe5\xa4\xa9\x00'
    src_text = dec_text.decode()        # 解码，得到对齐后的源文本：你好，明天<0x00>
    return src_text

