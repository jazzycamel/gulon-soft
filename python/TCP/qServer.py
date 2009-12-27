from sys import argv, exit
from PyQt4 import QtCore, QtGui, QtNetwork
from time import sleep

class ServerThread(QtCore.QThread):
    def __init__(self, socketDescriptor, parent):
        QtCore.QThread.__init__(self, parent)

        self.socketDescriptor = socketDescriptor
                        
    def run(self):
        self.tcpSocket = QtNetwork.QTcpSocket()
        self.tcpSocket.readyRead.connect(self.readStream)
        if not self.tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.emit(QtCore.SIGNAL("error(int)"), tcpSocket.error())
            return
            
        self.sendMsg('Hello World')
        #print self.tcpSocket.state()
        #sleep(5)
        #self.sendMsg('and again...')
        self.exec_()
                
    def sendMsg(self, data):
        data=data or 'Message'
        self.tcpSocket.writeData(data)
        self.tcpSocket.waitForBytesWritten()
        print "Written: ", data                              

    def readStream(self):
        data=self.tcpSocket.readLine()
        print "Received: ", data        
            
class Server(QtNetwork.QTcpServer):

    threadList=[]

    def __init__(self, parent=None):
        QtNetwork.QTcpServer.__init__(self, parent)

    def incomingConnection(self, socketDescriptor):
        thread = ServerThread(socketDescriptor, self)
        self.threadList.append(thread)
        #thread.finished.connect(thread.deleteLater)
        thread.start()

class ServerGUI(QtGui.QWidget):

    _running=False

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
              
        self.setGeometry(50,50,150,150)
        self.setWindowTitle('QServer')
        
        self.vLayout=QtGui.QVBoxLayout()
        self.setLayout(self.vLayout)
        
        self.specAddr=QtGui.QLineEdit('127.0.0.1')
        self.vLayout.addWidget(self.specAddr)
                
        self.specPort=QtGui.QLineEdit('5000')
        self.vLayout.addWidget(self.specPort)
        
        self.serverCtrl=QtGui.QPushButton('Start Server')
        self.serverCtrl.clicked.connect(self.ctrlServer)
        self.vLayout.addWidget(self.serverCtrl)        
        
        self.sendButton=QtGui.QPushButton('Send')
        #self.sendButton.clicked.connect(self.sendMsg)
        self.vLayout.addWidget(self.sendButton)
        
        self.serverTrace=QtGui.QTextEdit()
        self.vLayout.addWidget(self.serverTrace)
        
    def ctrlServer(self):    
        if not self._running:
            self._server = Server()
               
            if not self._server.listen(QtNetwork.QHostAddress(self.specAddr.text()),int(self.specPort.text())):
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
     
if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    server = ServerGUI()
    server.show()
    exit(app.exec_())