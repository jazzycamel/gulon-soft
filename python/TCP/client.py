from sys import argv, exit
from functools import wraps
from PyQt4.QtGui import QApplication, QWidget
from PyQt4.QtNetwork import QTcpSocket, QHostAddress

def message(method):
    message.messages.add(method.__name__)
    @wraps(method)
    def decorated(self, sender, *args, **kwargs):
        method(self, sender, *args, **kwargs)
    return decorated
message.messages=set()

class Client(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.socket=_s=QTcpSocket()
        _s.setSocketOption(QTcpSocket.LowDelayOption, 1) #Disable the Nagle Algorithm
        _s.connected.connect(self._connected)
        _s.connectToHost(QHostAddress(argv[1]), int(argv[2]))
        if not _s.waitForConnected(5000):
            print "Failed!"
            _s.close()

    def _connected(self):
        self._write("Hello World")

    def _write(self, d):
        self.socket.write("cmd:%s;" % d)
        while self.socket.waitForBytesWritten(): continue

if __name__=="__main__":
    if len(argv)<3: 
        print "Usage: python client.py <HOST> <PORT>"
        exit()
    a=QApplication(argv)
    c=Client()
    c.show()
    exit(a.exec_())
