from sys import argv

from PyQt4.QtNetwork import QUdpSocket
from PyQt4.QtGui import QApplication, QWidget, QTextEdit, QVBoxLayout, QIcon

class UdpRx(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle("UDP Receive")
        self.setGeometry(300,300,300,300)
        self.setWindowIcon(QIcon('g-square.png'))

        self.us=QUdpSocket(self)
        self.us.bind(5000)
        self.us.readyRead.connect(self.udpRead)

        self.trace=QTextEdit()
        self.trace.setReadOnly(True)
        self.trace.append("UDP Trace:")

        l=QVBoxLayout()
        l.addWidget(self.trace)

        self.setLayout(l)

    def udpRead(self):
        while self.us.hasPendingDatagrams():
            datagram, host, port=self.us.readDatagram(self.us.pendingDatagramSize())
            self.trace.append("%s:%s -> %s" % (host.toString(), port, datagram))
            if datagram.strip()=="::kill::":
                self.close()

app=QApplication(argv)
u=UdpRx()
u.show()
app.exec_()
