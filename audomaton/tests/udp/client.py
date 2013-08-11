import sip
sip.setapi("QString",2)
sip.setapi("QVariant",2)

from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
from os import environ
from random import randint

DISCOVERY_MESSAGE  = "DISC_MSG;"
DISCOVERY_RESPONSE = "DISC_RESP"

AUDOMATON_UDP_PORT = environ.get('AUDOMATON_UDP_PORT', 41513)

class Client(QObject):
    def __init__(self, parent=None, **kwargs):
        QObject.__init__(self, parent, **kwargs)

        self._socket=QTcpSocket(self)

        self._discovering=True
        self._discoverSocket=QUdpSocket(self, readyRead=self.discovered)
        while True:
            if self._discoverSocket.bind(randint(1000,99999), QUdpSocket.ShareAddress): break
        self.discover()

    @pyqtSlot()
    def discover(self):
        self._discoverSocket.writeDatagram(DISCOVERY_MESSAGE, QHostAddress.Broadcast, AUDOMATON_UDP_PORT)

    @pyqtSlot()
    def discovered(self):
        if not self._discovering: return
        
        while self._discoverSocket.hasPendingDatagrams():
            data,host,port=self._discoverSocket.readDatagram(self._discoverSocket.pendingDatagramSize())

            print "DISCOVER:", data, host.toString(), port

            if not data.endswith(';'): continue
            data=data[:-1]

            if not data.startswith(DISCOVERY_RESPONSE): continue

            _,tcp_port=data.split(':')

            print "TCP: {0}:{1}".format(host.toString(),tcp_port)

            self._discoverSocket.close()
            self._discovering=False

            if self._socket.state()==QAbstractSocket.UnconnectedState:
                self._socket.connectToHost(host,int(tcp_port))
                if not self._socket.waitForConnected(5000):
                    print "Failed to connect"

            break

if __name__=="__main__":
    from sys import argv, exit

    a=QCoreApplication(argv)
    c=Client()
    exit(a.exec_())