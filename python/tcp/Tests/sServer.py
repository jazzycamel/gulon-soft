from sys import argv, exit
from PyQt4 import QtCore, QtGui, QtNetwork

class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        QtNetwork.QTcpServer.__init__(self, parent)
        
    def incomingConnection(self, socketDescriptor):
        tcpSocket=QtNetwork.QTcpSocket()
        if not tcpSocket.setSocketDescriptor(socketDescriptor):
            print "Socket Error"
            return
            
        print "Server Running" 
        
        block = QtCore.QByteArray()
        outstr = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstr.setVersion(QtCore.QDataStream.Qt_4_0)
        outstr.writeUInt16(0)
        outstr << QtCore.QString("HelloWorld")
        outstr.device().seek(0)
        outstr.writeUInt16(block.count() - 2)
        
        tcpSocket.write(block)
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()
                        
app=QtGui.QApplication(argv)
server=Server()
server.listen(QtNetwork.QHostAddress('127.0.0.1'),5000)
app.exec_()            