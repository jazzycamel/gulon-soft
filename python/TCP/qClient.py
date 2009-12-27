from sys import argv
from time import sleep
from PyQt4 import QtCore, QtGui, QtNetwork

class ClientGUI(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(150,50,150,150)
        self.setWindowTitle('QClient')
        
        self.vLayout=QtGui.QVBoxLayout()
        self.setLayout(self.vLayout)

        self.specAddr=QtGui.QLineEdit('127.0.0.1')
        self.vLayout.addWidget(self.specAddr)
        
        self.specPort=QtGui.QLineEdit('5000')
        self.vLayout.addWidget(self.specPort)
                
        self.connButton=QtGui.QPushButton('Connect')
        self.connButton.clicked.connect(self.serverConnect)
        self.vLayout.addWidget(self.connButton)
        
        self.sendButton=QtGui.QPushButton('Send')
        self.sendButton.clicked.connect(self.sendMsg)
        self.vLayout.addWidget(self.sendButton)
        
    def serverConnect(self):    
        self.tcpSocket=QtNetwork.QTcpSocket(self)
        self.tcpSocket.readyRead.connect(self.readStream)
        self.tcpSocket.connectToHost(self.specAddr.text(), self.specPort.text().toInt()[0])
                       
    def readStream(self):
        data=self.tcpSocket.readLine()
        print data
        
    def sendMsg(self):
        data="Message"
        self.tcpSocket.writeData(data)
        self.tcpSocket.waitForBytesWritten()
        print "Written: ", data 
        
if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    client = ClientGUI()
    client.show()
    exit(app.exec_())        