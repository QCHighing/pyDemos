from db import SQL
from db import COLS
from ende import enc, dec


# '网站', '网址', '账号', '密码', '昵称', '邮箱', '备用'
class DBTASK(SQL):
    def __init__(self, key=None):
        super().__init__()
        self.key = key

    def complete(self):
        # print('数据库已关闭')
        self.close()

    def verify(self, password):
        admin = self.getall('AiProch')  # 取出加密后管理信息
        if admin:
            temp = enc(password, password) 
            if temp == admin[0][3]:
                return 1  # 1 - 密码正确，登录成功
            else:
                return 0  # 0 - 密码错误
        else:
            enckey = enc(password, password)  
            info = ['AiProch', '密码本', '', enckey]
            if self.insert(info):
                return 2  # 2 - 注册成功，加密后存入数据库
            else:
                return 3  # 3 - 数据库异常，数据插入失败

    def search(self, keyword):
        results = self.getall(keyword)
        for j, info in enumerate(results):
            results[j] = list(info)    # 元组转列表
            for i in range(2, 6):
                results[j][i] = dec(self.key, info[i])
        return results

    def dispall(self):
        return self.disp(COLS[0])

    def add(self, info):
        for i in range(2, 6):
            info[i] = enc(self.key, info[i])
        return self.insert(info)

    def del_task(self, web):
        return self.deldata(web)
