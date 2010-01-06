from sys import argv, exit
from PyQt4 import QtCore, QtGui, QtNetwork
from time import sleep


class ServerThread(QtCore.QThread):
    
    def __init__(self, socketDescriptor, rBuffer, clientID, parent):
        QtCore.QThread.__init__(self, parent)

        self.socketDescriptor = socketDescriptor
        self.rBuffer=rBuffer
        self.clientID=clientID
                        
    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.readyRead.connect(self.readStream)
        self.rBuffer.readyRead.connect(self.sendBuff)
        if not self.tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.emit(QtCore.SIGNAL("error(int)"), tcpSocket.error())
            return
        
        self.sendMsg('server,new,%s' % self.clientID)    
            
        self.exec_()
                
    def sendMsg(self, data):
        print self.tcpSocket.writeData(data+';')
        self.tcpSocket.waitForBytesWritten(1000)
        print "Written:", data                              
    
    def sendBuff(self):
        self.rBuffer.open(QtCore.QBuffer.ReadOnly)
        data=self.rBuffer.readLine()
        self.rBuffer.close()
        self.sendMsg(data)
        
    def readStream(self):
        data=self.tcpSocket.readLine()
        print "Received:", data        
            
class Server(QtNetwork.QTcpServer):

    threadList=[]
    bufferList=[]

    def __init__(self, parent=None):
        QtNetwork.QTcpServer.__init__(self, parent)
        self.parent=parent

    def incomingConnection(self, socketDescriptor):
        wBuffer = QtCore.QBuffer()
        self.threadID=str(len(self.threadList)+1)
        thread = ServerThread(socketDescriptor, wBuffer, self.threadID, self)
        self.bufferList.append(wBuffer)
        self.threadList.append(thread)
        if not self.parent.clientList.isEnabled():
            self.parent.clientList.setEnabled(True)
        self.parent.clientList.insertItem(int(self.threadID), QtCore.QString('Client '+self.threadID))
        self.parent.clientList.setItemData(int(self.threadID), QtCore.QVariant(self.threadID), 0)        
        thread.start()

    def sendMsg(self, msgt, args, client=None,):
        print "Sending..."
        clientID=self.parent.clientList.currentIndex()
        cBuffer=client or self.bufferList[clientID]
        if cBuffer.open(QtCore.QBuffer.WriteOnly):
            cBuffer.writeData('server,'+msgt+','+args)
            cBuffer.waitForBytesWritten(1000)
            cBuffer.close()
        else:
            print "Failed to Send"
        
class ServerGUI(QtGui.QWidget):

    _running=False
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
              
        self.setGeometry(50,50,150,150)
        self.setWindowTitle('QServer')
        #self.setWindowIcon(QtGui.QIcon('../../logo.png'))
        
        self.vLayout=QtGui.QVBoxLayout()
        self.setLayout(self.vLayout)
        
        self.specAddr=QtGui.QLineEdit('127.0.0.1')
        self.vLayout.addWidget(self.specAddr)
                
        self.specPort=QtGui.QLineEdit('5000')
        self.vLayout.addWidget(self.specPort)
        
        self.serverCtrl=QtGui.QPushButton('Start Server')
        self.serverCtrl.clicked.connect(self.ctrlServer)
        self.vLayout.addWidget(self.serverCtrl)        
        
        self.clientList=QtGui.QComboBox()
        self.clientList.setEnabled(False)
        self.vLayout.addWidget(self.clientList)
        
        self.sendButton=QtGui.QPushButton('Send')
        self.sendButton.clicked.connect(self.sendUserMsg)
        self.vLayout.addWidget(self.sendButton)
        
        self.killButton=QtGui.QPushButton('Kill Clients')
        self.killButton.clicked.connect(self.killClients)
        self.vLayout.addWidget(self.killButton)
        
        self.serverTrace=QtGui.QTextEdit()
        self.vLayout.addWidget(self.serverTrace)
        
    def ctrlServer(self):    
        if not self._running:
            self._server = Server(self)
               
            if not self._server.listen(QtNetwork.QHostAddress(self.specAddr.text()), self.specPort.text().toInt()[0]):
                print "Listen ERROR!"
                self.close()
                return
            else:
                print "Server Running"
                self.serverCtrl.setText('Stop Server')
                self._running=True    
        else:
            for thread in self._server.threadList:
                thread.exit()
            self._server.close()
            self.close()
     
    def killClients(self):
        for client in self._server.bufferList:
            self._server.sendMsg('kill','',client)
            
    def sendUserMsg(self):
        self._server.sendMsg('user','user message')                
            
if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    server = ServerGUI()
    server.show()
    exit(app.exec_())