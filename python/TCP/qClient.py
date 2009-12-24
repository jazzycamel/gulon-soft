from PyQt4 import QtNetwork

tcpSocket=QtNetwork.QTcpSocket()
tcpSocket.connectToHost("127.0.0.1",5000)
