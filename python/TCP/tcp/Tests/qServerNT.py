from sys import argv, exit
from PyQt4 import QtCore, QtGui, QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        QtNetwork.QTcpServer.__init__(self,parent)
        
    def incomingConnection(self, socketDescriptor):
        self.tcpSocket=QtNetwork.QTcpSocket()
        if not self.tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.emit(QtCore.SIGNAL("error(int)"), self.tcpSocket.error())
            return
        print self.tcpSocket.state()            
        
        
server=Server()
if not server.listen(QtNetwork.QHostAddress('127.0.0.1'),5000):
    print "Listen ERROR!"
    
while 1: pass
        