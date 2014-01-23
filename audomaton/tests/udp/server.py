import sip
sip.setapi("QString",2)
sip.setapi("QVariant",2)

from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
from os import environ

AUDOMATON_UDP_PORT = environ.get('AUDOMATON_UDP_PORT', 41513)
AUDOMATON_TCP_PORT = environ.get('AUDOMATON_TCP_PORT', 41514)

DISCOVERY_MESSAGE  = "DISC_MSG;"
DISCOVERY_RESPONSE = "DISC_RESP:{0};".format(AUDOMATON_TCP_PORT)

class Server(QTcpServer):
    def __init__(self, parent=None, **kwargs):
        QTcpServer.__init__(self,
            parent,
            newConnection=self.tcpHandler,
            **kwargs)

        self._sockets=[]

        if not self.listen(QHostAddress.Any, AUDOMATON_TCP_PORT): 
            print "Failed to listen!"
            qApp.quit()

        self._discoverSocket=QUdpSocket(self, readyRead=self.discover)
        print "Bind:", self._discoverSocket.bind(41513, QUdpSocket.ShareAddress)

    @pyqtSlot()
    def discover(self):
        print "Discover"
        while self._discoverSocket.hasPendingDatagrams():
            data,host,port=self._discoverSocket.readDatagram(self._discoverSocket.pendingDatagramSize())

            print "DISCOVER:", data, host.toString(), port

            if not data.startswith(DISCOVERY_MESSAGE): continue

            self._discoverSocket.writeDatagram(
                DISCOVERY_RESPONSE,
                host,
                port
            )

    @pyqtSlot()
    def tcpHandler(self):
        print "New connection..."
        s=self.nextPendingConnection()
        s.readyRead.connect(self.read)
        self._sockets.append(s)

    @pyqtSlot()
    def read(self): print "Socket message..."

if __name__=="__main__":
    from sys import argv, exit

    a=QCoreApplication(argv)
    s=Server()
    exit(a.exec_())