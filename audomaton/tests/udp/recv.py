import sip
sip.setapi("QString",2)
sip.setapi("QVariant",2)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

class Receiver(QDialog):
    def __init__(self, parent=None, **kwargs):
        QDialog.__init__(self, parent, **kwargs)

        self._messageNo=1

        l=QGridLayout(self)
        self._statusLabel=QLabel("Listening for broadcasted messages", self)
        l.addWidget(self._statusLabel, 0, 0, 1, 2)
        l.setColumnStretch(0,1)
        l.addWidget(QPushButton("&Quit", self, clicked=self.close), 1, 1)

        self._udpSocket=QUdpSocket(self, readyRead=self.processPendingDatagrams)
        self._udpSocket.bind(45454, QUdpSocket.ShareAddress)

    @pyqtSlot()
    def processPendingDatagrams(self):
        while self._udpSocket.hasPendingDatagrams():
            data,host,port=self._udpSocket.readDatagram(self._udpSocket.pendingDatagramSize())
            self._statusLabel.setText("Received: {0} ({1}:{2})".format(data,host.toString(),port))

            self._udpSocket.writeDatagram("Return {0}".format(self._messageNo), host, port)
            self._messageNo+=1

if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)
    r=Receiver()
    r.show()
    r.raise_()
    exit(a.exec_())