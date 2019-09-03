import os
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg

defaultIP = "192.168.1.103"
defaultPORT = "8888"


def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()        # 显示屏宽度
    screenheight = window.winfo_screenheight()      # 显示屏高度
    padleft = int((screenwidth - width) / 2)        # 左边距
    padup = int((screenheight - height) / 3)        # 上边距
    size = f'{width}x{height}+{padleft}+{padup}'
    return size


class Login(tk.Tk):
    def __init__(self):
        # 创建根窗口
        super().__init__()   # 继承父类的初始化方法
        self.title('远程管理')
        self.size = center_window(self, 500, 100)      # 长x宽
        self.geometry(self.size)
        self.resizable(width=True, height=False)  # 窗口大小固定
        # 创建容器
        self.frame = ttk.LabelFrame(self, text='请输入IP')
        self.frame.pack(fill='x', padx=20, pady=12)
        # 输入框
        self.value = tk.StringVar()
        self.value.set(defaultIP)  # 输入框的默认显示内容
        self.entry = ttk.Entry(self.frame, textvariable=self.value, font=('微软雅黑', 12))
        self.entry.pack(fill='x', padx=20, pady=12)
        # self.entry.focus_set()     # 当程序运行时,光标默认会出现在该文本框中
        # 绑定回车键，进行信息管理
        self.bind('<Return>', self.__connect)

    def __connect(self, event=None):
        self.ip = self.value.get()  # 获取输入的密码
        if self.ip is None:
            self.ip = defaultIP
        try:
            path = "ftp://" + self.ip + ":" + defaultPORT
            os.system(f"explorer.exe {path}")
            msg.showinfo(title='远程管理', message='远程管理启动成功，请稍后...')
        except Exception as e:
            err = 'ERROR!\n\n' + traceback.format_exc()
            msg.showerror(title='远程管理', message=err)

        self.focus_force()
        self.destroy()


def main():
    login = Login()     # 登录页面
    login.mainloop()


if __name__ == '__main__':
    main()
