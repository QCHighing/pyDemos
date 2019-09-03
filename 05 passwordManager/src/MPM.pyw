import task
from db import COLS
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg


def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()        # 显示屏宽度
    screenheight = window.winfo_screenheight()      # 显示屏高度
    padleft = int((screenwidth - width) / 2)        # 左边距
    padup = int((screenheight - height) / 3)        # 上边距
    size = f'{width}x{height}+{padleft}+{padup}'
    return size


class LOGIN(tk.Tk):
    def __init__(self):
        # 创建根窗口
        super().__init__()   # 继承父类的初始化方法
        self.title('AiProch 密码本')
        self.size = center_window(self, 500, 100)      # 长x宽
        self.geometry(self.size)
        self.resizable(width=True, height=False)  # 窗口大小固定
        # 创建容器 1
        self.frame = ttk.LabelFrame(self, text='请输入口令')
        self.frame.pack(fill='x', padx=20, pady=12)
        # 输入框
        self.value = tk.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.value, font=('微软雅黑', 12), show='●')
        self.entry.pack(fill='x', padx=20, pady=12)
        self.entry.focus_set()     # 当程序运行时,光标默认会出现在该文本框中
        # 创建数据库任务，即打开了数据库连接
        self.task = task.DBTASK()
        # 绑定回车键，进行信息管理
        self.bind('<Return>', self.__verify)
        # 窗口开/闭状态
        self.passflag = False
        # 绑定窗体关闭事件
        self.protocol("WM_DELETE_WINDOW", self.close)  # 窗体关闭事件绑定

    def __verify(self, event=None):
        self.focus_set()
        self.password = self.value.get()  # 获取输入的密码
        # print(self.value.get())
        retValue = self.task.verify(self.password)
        if retValue == 0:  # 密码错误
            msg.showerror(title='AiProch 密码本', message='密码错误！')
            self.value.set('')  # 清空输入框
            self.entry.focus_set()
        elif retValue == 3:  # 数据库异常
            msg.showerror(title='AiProch 密码本', message='数据库异常，程序已退出！')
            self.task.complete()
            exit(0)
        else:
            if retValue == 2:  # 首次登录
                msg.showinfo(title='AiProch 密码本', message=f'注册成功！\n管理密码：{self.password}\n请妥善保存')
            # else:
            #     msg.showinfo(title='AiProch 密码本', message='登录成功')
            self.passflag = True
            self.close()

    def close(self):
        self.task.complete()
        self.destroy()  # 窗口结束


class APP(tk.Tk):
    def __init__(self, key):
        # 创建根窗口
        super().__init__()   # 继承父类的初始化方法
        self.title('AiProch 密码本')
        self.size = center_window(self, 600, 300)      # 长x宽
        self.geometry(self.size)
        self.resizable(width=False, height=False)  # 窗口大小固定
        # 创建容器 1
        self.frame = ttk.LabelFrame(self, text='请输入网站/网址关键字：')
        self.frame.pack(fill='both', padx=20, pady=10)
        # 输入框
        self.value = tk.StringVar()
        self.entry = ttk.Entry(self.frame, width=56, textvariable=self.value, font=('微软雅黑', 12))
        self.entry.pack(fill='x', padx=20, pady=10)
        self.entry.focus_force()     # 强制获取光标
        # 绑定回车键，进行信息搜索
        self.bind('<Return>', self.cb_search)
        # 创建容器 2
        self.frame2 = ttk.Frame(self)
        self.frame2.pack()
        # 文本框
        self.text = tk.Text(self.frame2, width=46, height=8, font=('微软雅黑', 12))  # 宽度和行数
        self.text.pack(side='left', padx=20, pady=10)
        # self.text.config(state='disabled') # 禁止输入
        # 按钮
        ttk.Button(self.frame2, text='搜索', width=7, command=self.cb_search).\
            pack(side=tk.TOP, padx=15, pady=10)
        ttk.Button(self.frame2, text='清单', width=7, command=self.cb_dispall).\
            pack(side=tk.TOP, padx=15, pady=10)
        ttk.Button(self.frame2, text='添加', width=7, command=self.cb_add).\
            pack(side=tk.TOP, padx=15, pady=10)
        ttk.Button(self.frame2, text='删除', width=7, command=self.cb_delete).\
            pack(side=tk.TOP, padx=15, pady=10)
        # 创建数据库任务，即打开了数据库连接
        self.key = key
        self.task = task.DBTASK(self.key)
        # 绑定窗体关闭事件
        self.protocol("WM_DELETE_WINDOW", self.close)  # 窗体关闭事件绑定

    # 回车键按下，进行搜索和输出
    def cb_search(self, event=None):
        self.focus_set()
        self.text.delete('1.0','end')
        keyword = self.value.get()  # 获取输入的关键词
        results = self.task.search(keyword)
        if keyword and results:
            for infos in results:
                for i, info in enumerate(infos):
                    self.text.insert('end', f'{COLS[i]}：{info}\n')
                self.text.insert('end', '\n')
        else:
            msg.showinfo(title='AiProch 密码本', message='查无此项！\n请根据清单核对输入或添加新信息')
            self.value.set('')
            self.entry.focus_force()     # 强制获取光标

    # 清单
    def cb_dispall(self):
        self.text.delete('1.0','end')
        results = self.task.dispall()
        for web in results:
            self.text.insert('end', web[0]+'\n')

    # 添加（弹出顶级窗口）
    def cb_add(self):
        self.withdraw()                 # 窗口隐藏
        addw = TOP(self.key)            # 创建顶级窗口
        self.wait_window(window=addw)   # 等待直至顶级窗口关闭
        self.deiconify()                # 窗口显现
        self.entry.focus_force()        # 强制获取光标

    # 删除
    def cb_delete(self):
        if msg.askokcancel(title='AiProch 密码本', message='请确认是否删除当前条目？'):
            curweb = self.text.get('1.3', '1.end')
            if curweb == 'AiProch':
                msg.showerror(title='AiProch 密码本', message='数据加密相关信息，禁止删除！！\n自行删除，后果自负！')
            else:
                if self.task.del_task(curweb):
                    msg.showinfo(title='AiProch 密码本', message='删除成功！')
                    self.text.delete('1.0','end')
                    self.entry.focus_set()
                else:
                    msg.showerror(title='AiProch 密码本', message='条目不存在，删除失败')

    # 窗体关闭
    def close(self):
        self.task.complete()
        self.destroy()


class TOP(tk.Toplevel):
    def __init__(self,key):
        super().__init__()
        self.title('AiProch 密码本')
        self.size = center_window(self, 505, 300)      # 长x宽
        self.geometry(self.size)
        self.resizable(width=True, height=False)  # 窗口大小固定
        # 创建框架
        self.frame = ttk.LabelFrame(self, text='信息新增')
        self.frame.pack(side='left', padx=10, pady=10)
        # 标签与输入框
        self.values = []
        for i, col in enumerate(COLS, start=0):
            self.values.append(tk.StringVar())
            ttk.Label(self.frame, text=col, font=('微软雅黑', 10), width=5, anchor='center').\
                grid(row=i, column=0, padx=10, pady=5)
        self.web = ttk.Entry(self.frame, textvariable=self.values[0], font=('微软雅黑', 10), width=35)
        self.web.grid(row=0, column=1, padx=0, pady=5)
        self.web.focus_force()     # 当程序运行时,光标默认会出现在该文本框中
        for i in range(1, 7):
            ttk.Entry(self.frame, textvariable=self.values[i], font=('微软雅黑', 10), width=35).\
                grid(row=i, column=1, padx=0, pady=5)
        # 必填项标识
        for i in range(4):
            tk.Label(self.frame, text='*', font=('微软雅黑', 14), fg='red').\
                grid(row=i, column=2, padx=10, pady=5)
        # 按钮
        ttk.Button(self, text='确定', width=7, command=self.add2db).\
            pack(side=tk.BOTTOM, padx=0, pady=20,)
        ttk.Button(self, text='清空', width=7, command=self.clear).\
            pack(side=tk.BOTTOM, padx=0, pady=0,)
        self.protocol("WM_DELETE_WINDOW", self.close)  # 窗体关闭事件绑定
        # 创建数据库任务，即打开了数据库连接
        self.key = key
        self.task = task.DBTASK(self.key)
        # 绑定窗体关闭事件
        self.protocol("WM_DELETE_WINDOW", self.close)  # 窗体关闭事件绑定

    # 确定
    def add2db(self):
        info = []
        for value in self.values:
            info.append(value.get())
        # print(info)  # ['微**号', 'we**om', 'b**m', '**', '**', 'b**m', '微**号']
        if '' in info[:4]:
            msg.showerror(title='AiProch 密码本', message='必填项不能为空！')
        elif self.task.add(info):
            msg.showinfo(title='AiProch 密码本', message='信息录入成功！')
        else:
            msg.showerror(title='AiProch 密码本', message='数据存储发生错误，程序已停止！')
            exit(0)         # 无错误退出

    # 清空
    def clear(self):
        for value in self.values:
            value.set('')
        self.web.focus_set()

    # 窗体关闭
    def close(self):
        self.task.complete()
        self.destroy()


if __name__ == '__main__':
    login = LOGIN()     # 登录页面
    login.mainloop()
    if login.passflag:    # 登录窗口依旧开启
        app = APP(login.password)
        app.mainloop()      # 管理页面
