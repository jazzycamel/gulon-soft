from sys import argv, exit
from PyQt4 import QtCore, QtGui, QtNetwork


class ServerThread(QtCore.QThread):
    def __init__(self, socketDescriptor, parent):
        QtCore.QThread.__init__(self, parent)

        self.socketDescriptor = socketDescriptor
                
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.emit(QtCore.SIGNAL("error(int)"), tcpSocket.error())
            return
                      
class Server(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        QtNetwork.QTcpServer.__init__(self, parent)

    def incomingConnection(self, socketDescriptor):
        thread = ServerThread(socketDescriptor, self)
        thread.finished.connect(thread.deleteLater)
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
            self._server.close()
            self.close()
     
if __name__ == "__main__":
    app = QtGui.QApplication(argv)
    server = ServerGUI()
    server.show()
    exit(app.exec_())
