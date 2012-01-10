from sys import argv, exit
from PyQt4 import QtCore, QtGui, QtNetwork

class Client(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.blockSize=0
        self.tcpSocket=QtNetwork.QTcpSocket(self)
        self.tcpSocket.readyRead.connect(self.readSig)
        self.tcpSocket.connectToHost(QtNetwork.QHostAddress('127.0.0.1'), 5000)
        
    def readSig(self):
        instr = QtCore.QDataStream(self.tcpSocket)
        instr.setVersion(QtCore.QDataStream.Qt_4_0)
    
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return
            
            self.blockSize = instr.readUInt16()
        
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return
    
        nextFortune = QtCore.QString()
        instr >> nextFortune
        
        print nextFortune
        
app=QtGui.QApplication(argv)
client=Client()
client.show()
app.exec_()        
