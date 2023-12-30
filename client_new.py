import wx
import telnetlib
from time import sleep
import _thread as thread

class LoginFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)  # 设置窗口尺寸大小
        self.Center()  # 设置登录弹窗在桌面中心
        panel = wx.Panel(self)  # 创建一个面板，self表示实例即LoginFrame

        # 定义panel中的控件
        self.serverAddressLabel = wx.StaticText(panel, label="服务器地址")
        self.userNameLabel = wx.StaticText(panel, label="用户名")
        self.serverAddress = wx.TextCtrl(panel, value='127.0.0.1:6666')
        self.userName = wx.TextCtrl(panel)
        self.loginButton = wx.Button(panel, label='登录')

        # 定义一个横向的box1
        self.box1 = wx.BoxSizer()
        # 添加box1中的元素
        self.box1.Add(self.serverAddressLabel, proportion=5, flag=wx.EXPAND | wx.ALL,
                      border=5)  # 该元素占box1的比例为50%，方式为伸缩，边界为5
        self.box1.Add(self.serverAddress, proportion=5, flag=wx.EXPAND | wx.ALL, border=5)
        # 定义一个横向的box2
        self.box2 = wx.BoxSizer()
        # 添加box2中的元素
        self.box2.Add(self.userNameLabel, proportion=5, flag=wx.EXPAND | wx.ALL, border=5)
        self.box2.Add(self.userName, proportion=5, flag=wx.EXPAND | wx.ALL, border=5)
        # 定义一个纵向的v_box
        self.v_box = wx.BoxSizer(wx.VERTICAL)
        # 添加v_box中的元素
        self.v_box.Add(self.box1, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box1，比例为3
        self.v_box.Add(self.box2, proportion=3, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box2，比例为3
        self.v_box.Add(self.loginButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=30)  # 添加登录按钮，比例为3
        panel.SetSizer(self.v_box)

        # 绑定登录方法
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        self.Show()  # 显示以上控件

    def login(self, event):
        # 登录处理
        try:
            serverAddress = self.serverAddress.GetLineText(0).split(':')  # 获取serverAddress处的值并以:做为分隔符
            con.open(serverAddress[0], port=int(serverAddress[1]), timeout=10)  # 连接主机
            response = con.read_some()  # 接收服务端返回的数据
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))  # 通过write写给服务器端
            loginname = str(self.userName.GetLineText(0))  # 获取登录用户名称
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='多人聊天室 - ' + loginname, size=(500, 400))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (200, 150))

    def showDialog(self, title, content, size):
        # 显示错误信息对话框
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()

class ChatFrame(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title)
        self.Title = title
        self.SetSize(780, 500)  # 设置对话框的大小
        self.Center()  # 设置弹窗在屏幕中间

        panel = wx.Panel(self)
        # 定义panel中的控件
        # self.receiveLabel = wx.StaticText(panel, label="收到消息")
        self.receiveLabel = wx.StaticText(panel, label="消息")
        # self.sendLabel = wx.StaticText(panel, label="发出消息")
        self.noticeLabel = wx.StaticText(panel, label="系统通知")
        self.chatFrame1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT)
        # self.chatFrame2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RIGHT)
        self.noticeFrame = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(panel, value='')  # 设置发送消息的文本输入框的位置和尺寸
        self.toUser = wx.TextCtrl(panel, value='')  # 设置指定用户的文本输入框的位置和尺寸
        self.sendButton = wx.Button(panel, label="发送")
        self.sendDesignButton = wx.Button(panel, label="发送给指定用户")
        self.closeButton = wx.Button(panel, label="关闭聊天室")
        self.usersButton = wx.Button(panel, label="查询在线用户")

        # 定义横向的box1
        self.box1 = wx.BoxSizer()
        # 添加box1中的元素
        self.box1.Add(self.receiveLabel, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)  # 该元素占box1的比例为40%，方式为伸缩，边界为5
        # self.box1.Add(self.sendLabel, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box1.Add(self.noticeLabel, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)

        # 定义横向的box2
        self.box2 = wx.BoxSizer()
        # 添加box2中的元素
        self.box2.Add(self.chatFrame1, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)
        # self.box2.Add(self.chatFrame2, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)
        self.box2.Add(self.noticeFrame, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)

        # 定义横向的box3
        self.box3 = wx.BoxSizer()
        # 添加box3中的元素
        self.box3.Add(self.message, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)
        self.box3.Add(self.sendButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.box3.Add(self.usersButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        # 定义横向的box4
        self.box4 = wx.BoxSizer()
        # 添加box4中的元素
        self.box4.Add(self.toUser, proportion=6, flag=wx.EXPAND | wx.ALL, border=5)
        self.box4.Add(self.sendDesignButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        self.box4.Add(self.closeButton, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        # 定义一个纵向的v_box
        self.v_box = wx.BoxSizer(wx.VERTICAL)
        # 添加v_box中的元素
        self.v_box.Add(self.box1, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box1，比例为1
        self.v_box.Add(self.box2, proportion=7, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box2，比例为7
        self.v_box.Add(self.box3, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box3，比例为1
        self.v_box.Add(self.box4, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)  # 添加box4，比例为1
        panel.SetSizer(self.v_box)

        # 发送按钮绑定发送消息方法
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # 发送指定人按钮绑定方法
        self.sendDesignButton.Bind(wx.EVT_BUTTON, self.sendDesign)
        # Users按钮绑定获取在线用户数量方法
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # 关闭按钮绑定关闭方法
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        # 文本框绑定点击则清除文本内容的方法
        thread.start_new_thread(self.receive, ())  # 新增一个线程来处理接收服务器消息
        self.Show()

    def send(self, event):
        # 群发消息
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write(('say ' + message + '\n').encode("utf-8"))  # 通过write写给服务器端
            self.message.Clear()

    def sendDesign(self, event):
        # 给指定用户发送消息
        message = str(self.message.GetLineText(0)).strip()
        username = str(self.toUser.GetLineText(0)).strip()
        if message != '' and username != '':
            con.write(('DesignSay ' + message + '&' + username + '\n').encode("utf-8"))  # 通过write写给服务器端
            self.message.Clear()
            self.toUser.Clear()

    def lookUsers(self, event):
        # 查看当前在线用户
        con.write(b'look\n')

    def close(self, event):
        # 关闭窗口
        con.write(b'logout\n')
        con.close()  # Close the connection
        self.Close()

    def receive(self):
        # 接受服务器的消息
        title1 = self.Title.strip().split('-', 1)  # 去掉Title的左右空格后将Title按照-符号分隔开，获取到登录用户名
        loginname = title1[1].strip() + ':'  # 去掉登录名的左右空格,加上:符号，确保是该用户发送的消息

        while True:
            sleep(0.6)
            result = con.read_very_eager()  # 不断接收来自服务器的消息
            commandList = ['在线用户', '进入', '退出']  # 系统通知消息的指令
            for com in commandList:
                if com in result.decode('utf-8'):
                    self.noticeFrame.AppendText(result.decode('utf-8'))  # 将通知消息显示在noticeFrame中
                    break
            else:
                if loginname in str(result) or 'Username not exist' in str(result):  # 如果用户登录名在服务器发送的消息中可以查找到，即代表是本人发送的消息
                    self.chatFrame1.AppendText(result)  # 将聊天消息显示在本人的聊天窗口chatFrame2中
                    # self.chatFrame2.AppendText(result)  # 将聊天消息显示在本人的聊天窗口chatFrame2中
                else:
                    self.chatFrame1.AppendText(result)  # 否则将消息显示在别人消息的聊天窗口chatFrame1中


if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()  # 实例化一个telnet连接主机
    LoginFrame(None, -1, title="Login", size=(320, 250))  # id为-1表示主窗口
    app.MainLoop()  # 启动主循环
