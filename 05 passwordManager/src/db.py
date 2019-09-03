import sqlite3  # 导入数据库驱动

database = 'AiProch.db'
table = '密码本'
COLS = ['网站', '网址', '账号', '密码', '昵称', '邮箱', '备注']  # 表格 0-6 列


class SQL():
    def __init__(self):
        self.conn = sqlite3.connect(database)           # 连接到SQLite数据库，如果文件不存在，会自动在当前目录创建
        self.cursor = self.conn.cursor()                # 创建一个游标：Cursor
        self.cmd = f'''create table if not exists {table}
                    (   {COLS[0]}    varchar   primary key,
                        {COLS[1]}    varchar, 
                        {COLS[2]}    varchar, 
                        {COLS[3]}    varchar, 
                        {COLS[4]}    varchar, 
                        {COLS[5]}    varchar, 
                        {COLS[6]}    varchar
                    )'''
        self.cursor.execute(self.cmd)

    def close(self):
        self.cursor.close()                     # 关闭Cursor
        self.conn.commit()                      # 提交事务
        self.conn.close()                       # 关闭Connection

    # '网站', '网址', '账号', '密码', '昵称', '邮箱', '备注'
    def insert(self, col=[]):
        for n in range(7-len(col)):
            col.append('')
        self.cmd = f''' insert into {table} 
                        ({COLS[0]}, {COLS[1]}, {COLS[2]}, {COLS[3]}, {COLS[4]}, {COLS[5]}, {COLS[6]})
                        values
                        ('{col[0]}', '{col[1]}', '{col[2]}', '{col[3]}', '{col[4]}', '{col[5]}', '{col[6]}')
                    '''
        # self.cursor.execute(self.cmd)  # 调试所用，数据库异常则打开注释
        try:
            self.cursor.execute(self.cmd)
            self.conn.commit()                  # 提交事务
            return True
        except:
            # print('重复插入')
            return False

    # '网站', '网址', '账号', '密码', '昵称', '邮箱', '备注'
    def replace(self, col=[]):
        self.cmd = f''' replace into {table} 
                        ({COLS[0]}, {COLS[1]}, {COLS[2]}, {COLS[3]}, {COLS[4]}, {COLS[5]}, {COLS[6]})
                        values
                        ('{col[0]}', '{col[1]}', '{col[2]}', '{col[3]}', '{col[4]}', '{col[5]}', '{col[6]}')
                    '''
        self.cursor.execute(self.cmd)
        self.conn.commit()                  # 提交事务

    # '网站', '网址', '账号', '密码', '昵称', '邮箱', '备注'
    def getall(self, keyword):
        # 按照'网站'或 '网址'进行查找
        self.cmd = f''' select * 
                        from {table}
                        where {COLS[0]} like '%{keyword}%' 
                        or {COLS[1]} like '%{keyword}%'
                    '''
        self.cursor.execute(self.cmd)
        results = self.cursor.fetchall()
        return results

    # 输出所有网站名称
    def disp(self, col):
        self.cmd = f''' select {col}
                        from {table}
                    '''
        self.cursor.execute(self.cmd)
        results = self.cursor.fetchall()
        return results

    def deldata(self, web):
        self.cmd = f''' select *
                        from {table}
                        where {COLS[0]}='{web}'
                    '''
        self.cursor.execute(self.cmd)
        if  not self.cursor.fetchone():
            return False
        else:
            self.cmd = f''' delete 
                            from {table}
                            where {COLS[0]}='{web}'
                        '''
            self.cursor.execute(self.cmd)
            self.conn.commit()                      # 提交事务
            return True


