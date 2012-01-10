from sys import argv, exit
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtNetwork import QTcpServer, QHostAddress

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
        print _s.readLine().data()

if __name__=="__main__":
    if len(argv)<3: 
        print "Usage: python client.py <HOST> <PORT>"
        exit()
    a=QCoreApplication(argv)
    s=Server()
    a.exec_()
