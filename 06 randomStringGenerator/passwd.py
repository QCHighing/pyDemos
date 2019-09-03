import tkinter as tk
import tkinter.ttk as ttk
import random
import clipboard

nums = '0123456789'
strs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
chars = r'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''


def center_window(window, width, height):
    screenwidth = window.winfo_screenwidth()        # 显示屏宽度
    screenheight = window.winfo_screenheight()      # 显示屏高度
    padleft = int((screenwidth - width) / 2)        # 左边距
    padup = int((screenheight - height) / 3)        # 上边距
    size = f'{width}x{height}+{padleft}+{padup}'
    return size


class WINDOW(tk.Tk):
    def __init__(self):
        super(WINDOW, self).__init__()
        self.title('随机字符生成器')
        self.size = center_window(self, 420, 200)      # 长x宽
        self.geometry(self.size)
        self.resizable(width=False, height=False)  # 窗口大小固定

        # 第一行：
        # 框架1
        self.frame1 = ttk.LabelFrame(self, text='设置')
        self.frame1.pack(side='top', padx=30, pady=20)
        # 数字复选框
        self.numbutton = tk.BooleanVar()
        self.check1 = tk.Checkbutton(
            self.frame1, text='数字', variable=self.numbutton)
        self.check1.select()
        self.check1.pack(side='left', padx=20, pady=5)
        # 字母复选框
        self.strbutton = tk.BooleanVar()
        self.check2 = tk.Checkbutton(
            self.frame1, text='字母', variable=self.strbutton)
        self.check2.select()
        self.check2.pack(side='left', padx=20, pady=5)
        # 符号复选框
        self.chabutton = tk.BooleanVar()
        self.check3 = tk.Checkbutton(
            self.frame1, text='符号', variable=self.chabutton)
        self.check3.deselect()
        self.check3.pack(side='left', padx=20, pady=5)
        # 标签
        ttk.Label(self.frame1, text='长度').pack(side='left', padx=0, pady=5)
        # 输入框
        self.len = tk.StringVar()
        self.len.set(14)
        self.entry = ttk.Entry(self.frame1, width=2, textvariable=self.len)
        self.entry.pack(side='left', padx=5, pady=5)
        self.entry.focus_force()     # 强制获取光标
        # 空标签占位
        ttk.Label(self.frame1, text='').pack(side='left', padx=20, pady=5)

        # 第二行：
        # 文本框
        self.text = tk.Text(self, width=30, height=1,
                            font=('微软雅黑', 12))  # 宽度和行数
        self.text.pack(side='top', padx=30, pady=0)

        # 第三行：
        # 空标签占位
        ttk.Label(self, text='').pack(side='left', padx=50, pady=5)
        # 按钮1
        self.button1 = ttk.Button(self, text='生成', command=self.call_generate)
        self.button1.pack(side='left', padx=10, pady=20)
        # 按钮2
        self.button2 = ttk.Button(self, text='复制', command=self.call_copy)
        self.button2.pack(side='left', padx=10, pady=20)

    def call_generate(self):
        self.length = int(self.len.get())
        self.content = ''
        self.results = ''
        if self.numbutton.get():
            self.content += nums
        if self.strbutton.get():
            self.content += strs
        if self.chabutton.get():
            self.content += chars
        for i in range(self.length):
            self.results += random.choice(self.content)
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', self.results)

    def call_copy(self):
        clipboard.copy(self.text.get('1.0', 'end'))


if __name__ == '__main__':
    myWindow = WINDOW()
    myWindow.mainloop()
