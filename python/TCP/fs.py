import sys
import random
from PyQt4 import QtCore, QtGui, QtNetwork


class FortuneThread(QtCore.QThread):
    def __init__(self, socketDescriptor, fortune, parent):
        QtCore.QThread.__init__(self, parent)

        self.socketDescriptor = socketDescriptor
        self.text = fortune
        
    def run(self):
        tcpSocket = QtNetwork.QTcpSocket()
        if not tcpSocket.setSocketDescriptor(self.socketDescriptor):
            self.emit(QtCore.SIGNAL("error(int)"), tcpSocket.error())
            return
        
        block = QtCore.QByteArray()
        outstr = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        outstr.setVersion(QtCore.QDataStream.Qt_4_0)
        outstr.writeUInt16(0)
        outstr << self.text
        outstr.device().seek(0)
        outstr.writeUInt16(block.count() - 2)
        
        tcpSocket.write(block)
        tcpSocket.disconnectFromHost()
        tcpSocket.waitForDisconnected()

        
class FortuneServer(QtNetwork.QTcpServer):
    def __init__(self, parent=None):
        QtNetwork.QTcpServer.__init__(self, parent)

        self.fortunes = QtCore.QStringList()
        (self.fortunes << self.tr("You've been leading a dog's life. Stay off the furniture.")
             << self.tr("You've got to think about tomorrow.")
             << self.tr("You will be surprised by a loud noise.")
             << self.tr("You will feel hungry again in another hour.")
             << self.tr("You might have mail.")
             << self.tr("You cannot kill time without injuring eternity.")
             << self.tr("Computers are not intelligent. They only think they are."))

    def incomingConnection(self, socketDescriptor):
        fortune = self.fortunes[random.randint(0, self.fortunes.count()-1)]
        thread = FortuneThread(socketDescriptor, fortune, self)
        self.connect(thread, QtCore.SIGNAL("finished()"), thread, QtCore.SLOT("deleteLater()"))
        thread.start()


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.server = FortuneServer()
        
        self.statusLabel = QtGui.QLabel()
        self.quitButton = QtGui.QPushButton(self.tr("Quit"))
        self.quitButton.setAutoDefault(False)
        
        if not self.server.listen():
            QtGui.QMessageBox.critical(self, self.tr("Threaded Fortune Server"),
                                       self.tr("Unable to start the server: %1."
                                       .arg(self.server.errorString())))
            self.close()
            return
        
        self.statusLabel.setText(self.tr("The server is running on port %1.\n"\
                                         "Run the Fortune Client example now.")
                                         .arg(self.server.serverPort()))

        self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("close()"))
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.quitButton)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Threaded Fortune Server"))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(dialog.exec_())