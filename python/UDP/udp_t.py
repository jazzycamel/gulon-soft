from sys import argv

#from PyQt4.QtCore import 
from PyQt4.QtGui import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit
from PyQt4.QtNetwork import QUdpSocket, QHostAddress

class UdpTx(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle("UDP Transmit")
        #self.setGeometry(300,300,300,300)

        self.us=QUdpSocket(self)
        self.host=QHostAddress(QHostAddress.LocalHost)
        self.port=5000

        self.us.bytesWritten.connect(self.udpSent)

        send=QPushButton("&Send")
        send.clicked.connect(self.udpSend)

        self.datagram=QLineEdit()

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
