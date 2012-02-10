from sys import argv, exit
from functools import wraps
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtNetwork import QTcpServer, QHostAddress

def message(method):
    message.messages.add(method.__name__)
    @wraps(method)
    def decorated(self, sender, *args, **kwargs):
        method(self, sender, *args, **kwargs)
    return decorated
message.messages=set()

class Server(QTcpServer):
    _sockets=[]
    def __init__(self, parent=None):
        QTcpServer.__init__(self)

        self.newConnection.connect(self.handler)
        self.listen(QHostAddress(argv[1]), int(argv[2]))

    def handler(self):
        print "New connection..."
        _s=self.nextPendingConnection()
        _s.readyRead.connect(self.read)
        self._sockets.append(_s)

    def read(self):
        _s=self.sender()
        msg=_s.readLine().data()
        if not msg.endswith(";"):
            print "Message not correctly terminated."
            return
        else: msg=msg[:-1]
        data=msg.split(":")
        method=data[0]
        if method in message.messages: getattr(self, method)(*data[1:])
        else: print "Missing method: %s" % method

    @message
    def cmd(self, *args):
        print "Command: %s" % ",".join([arg for arg in args])

if __name__=="__main__":
    if len(argv)<3: 
        print "Usage: python client.py <HOST> <PORT>"
        exit()
    a=QCoreApplication(argv)
    s=Server()
    a.exec_()
