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
        
        self.msgText=QtGui.QLineEdit('Client Msg')
        self.vLayout.addWidget(self.msgText)
        
        self.sendButton=QtGui.QPushButton('Send')
        self.sendButton.clicked.connect(self.sendUserMsg)
        self.sendButton.setEnabled(False)
        self.vLayout.addWidget(self.sendButton)
        
    def serverConnect(self):    
        self.connButton.setText('Connecting...')
        self.connButton.setEnabled(False)
        self.tcpSocket=QtNetwork.QTcpSocket(self)
        self.tcpSocket.readyRead.connect(self.readStream)
        self.tcpSocket.connectToHost(self.specAddr.text(), self.specPort.text().toInt()[0])
        if not self.tcpSocket.waitForConnected(5000):
            print 'Failed to connect, error code:', self.tcpSocket.error()
            self.tcpSocket.close()
            self.close()
        self.connButton.setText('Connected')
        self.sendButton.setEnabled(True)
                       
    def readStream(self):
        data=self.tcpSocket.readLine()
        print "Received: ", data
        
        msgs=data.split(';')
        
        for msg in msgs:
            if not msg=='':
                print msg
                sender, msgt, args = msg.split(',')
                if sender=='server' and msgt=='new':
                    self.clientID=args
                    self.setWindowTitle("QClient: %s" % self.clientID)
                if sender=='server' and msgt=='kill':
                    self.sendMsg('dead','')
                    self.tcpSocket.close()
                    self.close()
                else:
                    pass
    
    def sendUserMsg(self):
        self.sendMsg('user',self.msgText.text())
            
    def sendMsg(self,msg,args):
        message=self.clientID+','+msg+','+args
        self.tcpSocket.writeData(message)
        self.tcpSocket.waitForBytesWritten()
        print "Written: ", msg, args 
        
if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    client = ClientGUI()
    client.show()
    exit(app.exec_())        