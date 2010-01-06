from sys import argv
from PyQt4 import QtCore, QtGui

class BuffApp(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.msgBuff=QtCore.QBuffer()
        self.msgBuff.readyRead.connect(self.msgRecv)
        
        self.setGeometry(50,50,200,200)
        self.setWindowTitle('QBuffer')
        self.vLayout=QtGui.QVBoxLayout()
        self.setLayout(self.vLayout)
        
        self.msgbox=QtGui.QLineEdit('Message')
        self.vLayout.addWidget(self.msgbox)
        
        self.button=QtGui.QPushButton('Write')
        self.button.clicked.connect(self.buffWrite)
        self.vLayout.addWidget(self.button)
        
        self.recvbox=QtGui.QLineEdit()
        self.vLayout.addWidget(self.recvbox)
        
    def buffWrite(self):
        self.msgBuff.open(QtCore.QBuffer.WriteOnly)
        self.msgBuff.writeData(self.msgbox.text())
        self.msgBuff.close()
        print 'Written:', self.msgbox.text()
        
    def msgRecv(self):
        self.msgBuff.open(QtCore.QBuffer.ReadOnly)
        data=self.msgBuff.readLine()
        self.msgBuff.close()
        print 'Received', data
              
app=QtGui.QApplication(argv)
buffApp=BuffApp()
buffApp.show()
app.exec_()        