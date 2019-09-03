import sqlite3  # 导入数据库驱动


# 数据库相关全局变量
database = 'ProxyPool.db'
table = 'PROXY'
conn = None
cursor = None


def start():
    global conn, cursor
    conn = sqlite3.connect(database)   # 连接到SQLite数据库，如果文件不存在，会自动在当前目录创建
    cursor = conn.cursor()              # 创建一个游标：Cursor
    # 执行一条SQL语句，(表不存在时)创建表
    cursor.execute('''create table if not exists %s
                       (IP          varchar(10) primary key,
                        PORT        varchar(10),
                        ADDR        varchar(10),
                        ANONYMOUS   varchar(10),
                        TYPE        varchar(10),
                        STATUS      varchar(10),
                        TIME        varchar(10))
                   ''' % table)


def commit():
    conn.commit()                      # 提交事务


def close():
    global conn, cursor
    cursor.close()                     # 关闭Cursor
    conn.commit()                      # 提交事务
    conn.close()                       # 关闭Connection


def insert(ip, port, addr, anonymous=None, types=None, status='未知', time=None):
    global conn, cursor
    sql = '''insert into %s
             (IP, PORT, ADDR, ANONYMOUS, TYPE, STATUS, TIME)
             values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
          ''' % (table, ip, port, addr, anonymous, types, status, time)
    try:
        cursor.execute(sql)
        print()
        return True
    except:
        return False


def update(ip, rowName, value):
    global conn, cursor
    sql = '''update %s
             set %s = '%s'
             where IP='%s'
          ''' % (table, rowName, value, ip)
    cursor.execute(sql)
    conn.commit()                      # 提交事务


# [0 - 6]：('000.000.0.000', '8888', '爬取时间', 'None', 'None', '未知', '2018-06-25 20:52:43')
def get(ip=None):
    global conn, cursor
    if ip:
        sql = '''select *
                 from %s
                 where IP='%s'
              ''' % (table, ip)
    else:   # 随机获取有效代理
        sql = '''select IP,PORT from %s
                 where STATUS='有效代理' or STATUS='未知'
                 order by random()
                 limit 1
              ''' % table
    cursor.execute(sql)
    return cursor.fetchone()


def delete(ip):
    global conn, cursor
    sql = '''delete from %s
             where IP='%s'
          ''' % (table, ip)
    cursor.execute(sql)
    conn.commit()                      # 提交事务
