import sip
sip.setapi("QString",2)
sip.setapi("QVariant",2)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

class Sender(QDialog):
    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self, parent, **kwargs)

        self._messageNo=1

        l=QVBoxLayout(self)

        self._statusLabel=QLabel("Ready to broadcast datagrams on port 45454", self)
        l.addWidget(self._statusLabel)

        self._replyLabel=QLabel(self)
        l.addWidget(self._replyLabel)

        self._startButton=QPushButton("&Start", self, clicked=self.startBroadcasting)
        self._quitButton=QPushButton("&Quit", self, clicked=self.close)
        bb=QDialogButtonBox(self)
        bb.addButton(self._startButton, QDialogButtonBox.ActionRole)
        bb.addButton(self._quitButton, QDialogButtonBox.RejectRole)
        l.addWidget(bb)

        self._udpSocket=QUdpSocket(self, readyRead=self.processPendingDatagrams)
        self._udpSocket.bind(45455)

    def timerEvent(self, event):
        self._statusLabel.setText("Now broadcasting datagram {0}".format(self._messageNo))
        self._udpSocket.writeDatagram("Broadcast message {0}".format(self._messageNo), QHostAddress.Broadcast, 45454)
        self._messageNo+=1

    @pyqtSlot()
    def startBroadcasting(self): self.startTimer(1000)

    @pyqtSlot()
    def processPendingDatagrams(self):
        while self._udpSocket.hasPendingDatagrams():
            data,host,port=self._udpSocket.readDatagram(self._udpSocket.pendingDatagramSize())
            self._replyLabel.setText("Received: {0} ({1}:{2})".format(data,host.toString(),port))


if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)
    s=Sender()
    s.show()
    s.raise_()
    exit(a.exec_())