# -*-coding:utf-8-*-
import asynchat
import asyncore

# 定义端口
PORT = 6666


# 定义结束异常类
class EndSession(Exception):
    pass


class ChatServer(asyncore.dispatcher):
    # dispatcher是asyncore中一个socket框架，为socket添加一些通用的回调方法
    """
    聊天服务器
    """

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        # 创建socket
        self.create_socket()
        # 设置 socket 为可重用
        self.set_reuse_addr()
        # 监听端口
        self.bind(('', port))
        self.listen(5)
        self.users = {}  # 初始化用户
        self.main_room = ChatRoom(self)  # 定义聊天室

    def handle_accept(self):
        conn, addr = self.accept()  # accept()会等待并返回一个客户端的连接
        ChatSession(self, conn)


class ChatSession(asynchat.async_chat):
    # 负责和客户端通信
    def __init__(self, server, sock):
        #         print(server,sock)
        # server:<__main__.ChatServer listening :6666 at 0x2994860>
        # sock:<socket.socket fd=204, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 6666), raddr=('127.0.0.1', 52148)>
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator(b'\n')  # 定义终止符
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        # 从当前房间移除自身，然后添加到指定房间
        try:
            cur = self.room
        except AttributeError:  # 该错误是python找不到对应的对象的属性
            pass
        else:
            cur.remove(self)  # 如果try内的语句正常执行，接着执行else里的语句
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):  # 接收客户端的数据
        self.data.append(data.decode("utf-8"))

    def found_terminator(self):  # 当客户端的一条数据结束时的处理
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line.encode("utf-8"))
        # 退出聊天室的处理
        except EndSession:
            self.handle_close()

    def handle_close(self):  # 当session关闭时，将进入logoutRoom
        asynchat.async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


class CommandHandler:  # 命令处理类
    def unknown(self, session, cmd):
        # 响应未知命令
        # 通过aynchat.async_chat.push方法发送消息
        session.push(('Unknown command {} \n'.format(cmd)).encode('utf-8'))

    def handle(self, session, line):
        line = line.decode()
        # print(f"line{line}")
        # 命令处理
        if not line.strip():  # 如果line去掉左右空格后为空
            return
        parts = line.split(' ', 1)  # 以空格为分隔符，分隔成两个
        cmd = parts[0]
        # print(f"parts:{parts}")
        # print(f"cmd:{cmd}")
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        # 通过协议代码执行相应的方法
        method = getattr(self, 'do_' + cmd,
                         None)  # getattr()函数用于返回一个对象属性值。class A(object):bar = 1 >>>a = A(),getattr(a, 'bar')# 获取属性 bar值=1
        #         print(method)
        try:
            method(session, line)  # 跳转到对应的方法，如do_look,do_say
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandler):
    # 包含多个用户的环境，负责基本的命令处理和广播
    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        # 一个用户进入房间
        self.sessions.append(session)

    def remove(self, session):
        # 一个用户离开房间
        self.sessions.remove(session)

    def broadcast(self, line):
        # 向所有用户发送指定消息
        # 使用asynchat.async_chat.push方法发送数据
        for session in self.sessions:
            session.push(line)

    def sendDesignMsg(self, msg, sendpeople, topeople):
        # 对指定用户发送消息
        print(sendpeople, topeople, self.sessions, self.server.users)
        if topeople in self.server.users:
            session1 = self.server.users[sendpeople]  # 获取发信人的session
            session2 = self.server.users[topeople]  # 获取收信人的session
            session1.push(msg)  # 发信人和收信人的聊天页面均显示消息
            session2.push(msg)
        else:
            session = self.server.users[sendpeople]
            session.push(b'Username not exist\n')

    def do_logout(self, session, line):
        # 退出房间
        raise EndSession


class LoginRoom(Room):
    # 处理登录用户
    def add(self, session):
        # 用户连接成功的回应
        Room.add(self, session)
        # 使用asynchat.async_chat.push方法发送数据
        '''
        Python3的字符串的编码语言用的是unicode编码，由于Python的字符串类型是str，
            在内存中以Unicode表示，一个字符对应若干字节，如果要在网络上传输，
            或保存在磁盘上就需要把str变成以字节为单位的bytes
        python对bytes类型的数据用带b前缀的单引号或双引号表示：
        '''
        session.push(b'Connect Success')

    def do_login(self, session, line):
        # 用户登录逻辑
        name = line.strip()
        # 获取用户名称
        if not name:
            session.push(b'UserName Empty')
        # 检查是否是同名用户
        elif name in self.server.users:
            session.push(b'UserName Exist')
        else:
            session.name = name
            session.enter(self.server.main_room)


class LogoutRoom(Room):
    # 处理退出用户
    def add(self, session):
        # 从服务器中移除
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatRoom(Room):
    # 聊天用的房间
    def add(self, session):
        # 广播新用户进来
        session.push(b'Login Success')
        self.broadcast((session.name + ' has entered the room.\n').encode('utf-8'))
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        # 广播用户离开
        Room.remove(self, session)
        self.broadcast((session.name + ' has left the room.\n').encode('utf-8'))

    def do_say(self, session, line):
        # 发送消息
        self.broadcast((session.name + ':' + line + '\n').encode('utf-8'))

    def do_DesignSay(self, session, line):
        # 发送消息给指定的用户
        words = line.split('&', 1)  # 以&为分隔符，分隔成两个，发送的消息和指定收信人的姓名
        print(words)

        msg = words[0]  # 获取发送消息内容
        topeople = words[1]  # 获取收信人名称
        sendpeople = session.name  # 获取发信人的名称
        print(msg, topeople, sendpeople)
        self.sendDesignMsg((session.name + ':' + msg + '\n').encode('utf-8'), sendpeople, topeople)

    def do_look(self, session, line):
        # 查看在线用户
        session.push(b'Online Users:\n')
        for other in self.sessions:
            session.push((other.name + '\n').encode('utf-8'))


if __name__ == '__main__':
    s = ChatServer(PORT)
    try:
        print("chat serve run at '127.0.0.1:{0}'".format(PORT))
        asyncore.loop()
    except KeyboardInterrupt:
        print('chat server exit')
