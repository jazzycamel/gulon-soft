from sys import argv

from PyQt4.QtGui import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QIcon
from PyQt4.QtNetwork import QUdpSocket, QHostAddress

class UdpTx(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle("UDP Transmit")
        self.setWindowIcon(QIcon('g-square.png'))

        self.us=QUdpSocket(self)
        self.host=QHostAddress(QHostAddress.LocalHost)
        self.port=5000

        self.us.bytesWritten.connect(self.udpSent)

        send=QPushButton("&Send")
        send.clicked.connect(self.udpSend)

        self.datagram=QLineEdit()
        self.datagram.returnPressed.connect(self.udpSend)

        l=QVBoxLayout()
        l.addWidget(self.datagram)
        l.addWidget(send)

        self.setLayout(l)

    def udpSend(self):
        print self.us.writeDatagram(self.datagram.text(), self.host, self.port)

    def udpSent(self):
        print "Datagram sent"


app=QApplication(argv)
u=UdpTx()
u.show()
app.exec_()
