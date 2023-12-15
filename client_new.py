import wx
import telnetlib
from time import sleep
import _thread as thread


class LoginFrame(wx.Frame):
    """
    登录窗口
    """

    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)  # 设置窗口尺寸大小
        self.Center()  # 设置登录弹窗在桌面中心

        # 使用尺寸器改写,改写后拉大或者缩小窗口，中间的控件会随着窗口的大小已固定的尺寸而改变
        panel = wx.Panel(self)  # 创建一个面板，self表示实例即LoginFrame

        # 定义panel中的控件
        self.serverAddressLabel = wx.StaticText(panel, label="Server Address")
        self.userNameLabel = wx.StaticText(panel, label="UserName")
        self.serverAddress = wx.TextCtrl(panel)
        self.userName = wx.TextCtrl(panel)
        self.loginButton = wx.Button(panel, label='Login')

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
            con.open(serverAddress[0], port=int(serverAddress[1]), timeout=10)  # open方法连接主机
            response = con.read_some()  # 接收服务端返回的数据
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))  # 通过write写给服务器端
            loginname = str(self.userName.GetLineText(0))  # 获取登录用户名称
            #             print(loginname)
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='ShiYanLou Chat Client - ' + loginname, size=(500, 400))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (200, 150))

    def showDialog(self, title, content, size):
        # 显示错误信息对话框
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()  # showModal() 方法用于显示对话窗口


class ChatFrame(wx.Frame):
    """
    聊天窗口
    """

    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        self.Title = title  # 'ShiYanLou Chat Client - '+self.loginname
        self.SetSize(780, 500)  # 设置对话框的大小
        self.Center()  # 设置弹窗在屏幕中间

        # 使用尺寸器改写,改写后拉大或者缩小窗口，中间的控件会随着窗口的大小已固定的尺寸而改变
        panel = wx.Panel(self)  # 创建一个面板，self表示实例即ChatFrame
        # 定义panel中的控件
        self.receiveLabel = wx.StaticText(panel, label="Receive Msg")
        self.sendLabel = wx.StaticText(panel, label="Send Msg")
        self.noticeLabel = wx.StaticText(panel, label="Notice")
        self.chatFrame1 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT)
        self.chatFrame2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RIGHT)
        self.noticeFrame = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(panel, value='input message')  # 设置发送消息的文本输入框的位置和尺寸
        self.toUser = wx.TextCtrl(panel, value='input username')  # 设置指定用户的文本输入框的位置和尺寸
        self.sendButton = wx.Button(panel, label="Send")
        self.sendDesignButton = wx.Button(panel, label="SendDesign")
        self.closeButton = wx.Button(panel, label="Close")
        self.usersButton = wx.Button(panel, label="Online")

        # 定义横向的box1
        self.box1 = wx.BoxSizer()
        # 添加box1中的元素
        self.box1.Add(self.receiveLabel, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)  # 该元素占box1的比例为40%，方式为伸缩，边界为5
        self.box1.Add(self.sendLabel, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box1.Add(self.noticeLabel, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        # 定义横向的box2
        self.box2 = wx.BoxSizer()
        # 添加box2中的元素
        self.box2.Add(self.chatFrame1, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box2.Add(self.chatFrame2, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
        self.box2.Add(self.noticeFrame, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

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
            con.write(('DesignSay ' + message + ' ' + username + '\n').encode("utf-8"))  # 通过write写给服务器端
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
            commandList = ['Online Users', 'entered', 'left']  # 系统通知消息的指令
            for com in commandList:
                if com in str(result):
                    self.noticeFrame.AppendText(result)  # 将通知消息显示在noticeFrame中
                    break
            else:
                if loginname in str(result) or 'Username not exist' in str(
                        result):  # 如果用户登录名在服务器发送的消息中可以查找到，即代表是本人发送的消息
                    self.chatFrame2.AppendText(result)  # 将聊天消息显示在本人的聊天窗口chatFrame2中
                else:
                    self.chatFrame1.AppendText(result)  # 否则将消息显示在别人消息的聊天窗口chatFrame1中


if __name__ == '__main__':
    app = wx.App()  # 实例化一个主循环
    # 聊天协议基于文本，和服务器之间的通信将基于 telnetlib模块实现
    # 连接主机----两种方法，
    # 一种是在实例化时传入ip地址连接主机（con = telnetlib.Telnet(host_ip,port=23)）
    # 第二种是，先不传参数进行实例化再用open方法连接主机
    con = telnetlib.Telnet()  # 实例化一个telnet连接主机
    LoginFrame(None, -1, title="Login", size=(320, 250))  # id为-1表示主窗口
    app.MainLoop()  # 启动主循环
