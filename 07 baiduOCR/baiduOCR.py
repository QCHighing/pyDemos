import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from PIL import ImageGrab
from time import sleep
from aip import AipOcr
import clipboard
import os

mode = 0
breakFlag = 0
# 文字识别


def OCR(fileName, mode=0):
    # 定义常量
    APP_ID = '您的 APP_ID'
    API_KEY = '您的 API_KEY'
    SECRET_KEY = '您的 SECRET_KEY'
    # 初始化AipFace对象
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 读取图片
    with open(fileName, 'rb') as fp:
        image = fp.read()
    # 通用文字识别
    if mode == 0:
        """ 可选参数 """
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        # 调用通用文字识别, 图片参数为本地图片
        results = client.basicGeneral(image, options)
        '''结果示例
        {
        "log_id": 2471272194,
        "words_result_num": 2,
        "words_result":
            [
                {"words": " TSINGTAO"},
                {"words": "青島睥酒"}
            ]
        }
        '''
    # 高精度文字识别
    else:
        """ 参数 """
        options = {}
        options["detect_direction"] = "true"
        options["probability"] = "true"
        """ 带参数调用通用文字识别（高精度版） """
        results = client.basicAccurate(image, options)
        '''结果示例
        {
        'log_id': 341147315111859960,
        'direction': 0,
        'words_result_num': 4,
        'words_result':
            [
                {'words': ' OPEN FILES',
                 'probability':{'variance': 1e-06,
                                'average': 0.971955,
                                'min': 0.971142}
                }
            ]
        }
        '''
    chars = results.get("words_result", None)
    for x in chars:
        yield x.get("words", None)


class ScreenShot(tk.Toplevel):
    def __init__(self, png):
        super(ScreenShot, self).__init__()
        self.screenWidth = self.winfo_screenwidth()        # 显示屏宽度
        self.screenHeight = self.winfo_screenheight()      # 显示屏高度
        self.overrideredirect(True)  # 不显示最大化、最小化按钮
        self.canvas = tk.Canvas(
            self, bg='white', width=self.screenWidth, height=self.screenHeight)
        self.image = tk.PhotoImage(file=png)
        self.canvas.create_image(
            self.screenWidth // 2, self.screenHeight // 2, image=self.image)  # 截图放置在中心位置
        self.rectangle = self.canvas.create_rectangle(
            0, 0, 0, 0, outline='red')  # 初始矩形
        self.canvas.pack(fill='x', expand='yes')
        # 获取焦点
        self.canvas.focus_force()     # 强制获取光标
        # 绑定鼠标左键
        self.canvas.bind('<Button-1>', self.onLeftButtonDown)
        # 绑定鼠标拖动
        self.canvas.bind("<B1-Motion>", self.onLeftButtonMove)
        # 绑定回车键
        self.bind('<Return>', self.onEnterKeyDown)
        # 绑定ESC键
        self.bind('<Escape>', self.onEscDown)

    def onLeftButtonDown(self, event):
        self.x1 = event.x
        self.y1 = event.y

    def onLeftButtonMove(self, event):
        self.x2 = event.x
        self.y2 = event.y
        self.canvas.coords(
            self.rectangle, (self.x1, self.y1, self.x2, self.y2))
        self.bbox = [self.x1, self.y1, self.x2, self.y2]

    def onEnterKeyDown(self, ecent=None):
        # 保证坐标的大小次序
        if self.x1 > self.x2:
            self.bbox[0], self.bbox[2] = self.bbox[2], self.bbox[0]
        if self.y1 > self.y2:
            self.bbox[1], self.bbox[3] = self.bbox[3], self.bbox[1]
        # 区域截图
        self.im = ImageGrab.grab(self.bbox)
        self.im.save('temp.png')    # 保存截图
        self.im.close()
        self.destroy()

    def onEscDown(self,event=None):
        global breakFlag
        breakFlag = 1
        self.destroy()

class DispWin(tk.Toplevel):
    def __init__(self):
        super(DispWin, self).__init__()
        self.frame = ttk.LabelFrame(self, text='识别结果')
        self.frame.pack()
        self.scrt = scrolledtext.ScrolledText(
            self.frame, width=60, height=15, wrap=tk.WORD)
        self.scrt.pack()
        self.scrt.delete('1.0', 'end')
        # 识别并展示
        for ch in OCR('temp.png', mode):
            self.scrt.insert('end', ch + '\n')
        ttk.Button(self, text='关闭', command=self.closeDisp).pack(
            side='right', padx=10, pady=20)
        ttk.Button(self, text='复制', command=self.copyText).pack(
            side='right', padx=10, pady=20)

    def copyText(self):
        clipboard.copy(self.scrt.get('1.0', 'end'))

    def closeDisp(self):
        self.destroy()

class WINDOW(tk.Tk):
    def __init__(self):
        super(WINDOW, self).__init__()
        self.title('简易OCR')
        self.geometry('300x130')
        # self.resizable(width=False, height=False)  # 窗口大小固定
        # 按钮
        self.button = ttk.Button(self, text='开始截图识别', command=self.callback).place(
            width=130, height=50, relx=0.25, rely=0.1)
        # 单选框组
        self.Mod_Button = tk.IntVar()
        self.check1 = tk.Radiobutton(
            self, text='通用识别', variable=self.Mod_Button, value=0)
        self.check1.select()
        self.check1.place(relx=0.2, rely=0.5)
        self.check2 = tk.Radiobutton(
            self, text='精准识别', variable=self.Mod_Button, value=1)
        self.check2.place(relx=0.5, rely=0.5)
        # 提示标签
        ttk.Label(self, text='使用步骤：1-鼠标拖动；2-按下回车键', font=('微软雅黑', 12)).\
            pack(side='bottom', pady=15)
        # 绑定ESC键
        self.bind('<Escape>', self.close)
        # 绑定窗体关闭事件
        self.protocol("WM_DELETE_WINDOW", self.close)
        # 中途退出标志
        breakFlag = 0

    def callback(self):
        global mode, breakFlag
        mode = self.Mod_Button.get()
        self.withdraw()  # 窗口隐藏
        sleep(0.5)  # 等待窗口隐藏成功
        self.im = ImageGrab.grab()  # 全屏截图
        self.im.save('temp.png')    # 保存截图
        self.im.close()
        topwin = ScreenShot('temp.png')  # 可变参数传入可输出
        self.wait_window(window=topwin)   # 等待直至顶级窗口关闭
        if not breakFlag:
            topdisp = DispWin()
            self.wait_window(window=topdisp)   # 等待直至顶级窗口关闭
        breakFlag = 0
        self.deiconify()  # 窗口显现

    def close(self,event=None):
        if os.path.isfile(os.path.join('temp.png')):
            os.remove('temp.png')  # 删除文件
        self.destroy()
        exit(0)

if __name__ == '__main__':
    myWindow = WINDOW()
    myWindow.mainloop()
