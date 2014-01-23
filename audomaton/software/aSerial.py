import sip
sip.setapi('QString',2)
sip.setapi('QVariant',2)

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import serial
from serial.tools import list_ports

__all__=['aSerial']

BAUDRATES=[50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

class SerialWorker(QObject):
    dataAcquired=pyqtSignal(str)
    opened=pyqtSignal()
    closed=pyqtSignal()
    bytesWritten=pyqtSignal(int)

    def __init__(self, port, baud, parent=None, **kwargs):
        QObject.__init__(self, parent, **kwargs)

        self._serial=None
        self._timeout=0
        self._timerId=None

        self._port=port
        self._baud=baud

    @pyqtSlot()
    def open(self):
        self._serial=serial.Serial(self._port, self._baud, timeout=self._timeout)        
        self._timerId=self.startTimer(1)
        self.opened.emit()

    @pyqtSlot()
    def close(self):
        self.killTimer(self._timerId)
        self._serial.close()
        self.closed.emit()

    def timerEvent(self, event):
        if self._timerId!=event.timerId(): return
        data=self._serial.read(1024)
        if not len(data): return
        self.dataAcquired.emit(data)

    @pyqtSlot(str)
    def write(self, data):
        data=str(data)
        _bytes=self._serial.write(data)
        self.bytesWritten.emit(_bytes)

class aSerial(QIODevice):
    _close=pyqtSignal()
    _write=pyqtSignal(str)

    def __init__(self, port, baud, parent=None, **kwargs):
        QIODevice.__init__(self, parent, **kwargs)

        self._open=False
        self._openMode=QIODevice.NotOpen
        self._thread=None
        self._worker=None
        self._data=""

        self._port=port
        self._baud=baud

    def openMode(self): return self._openMode

    def open(self, mode):
        if self._open or mode!=QIODevice.ReadWrite: return False
        self._openMode=mode

        self._thread=QThread(self, finished=self._threadFinished)
        self._worker=SerialWorker(
            self._port,
            self._baud,
            opened=self._opened,
            closed=self._closed,
            dataAcquired=self._dataAcquired,
            bytesWritten=self._bytesWritten
        )

        self._thread.started.connect(self._worker.open)
        self._worker.closed.connect(self._thread.quit)
        self._close.connect(self._worker.close)
        self._write.connect(self._worker.write)

        self._worker.moveToThread(self._thread)
        self._thread.start()

    def isOpen(self): return self._open

    @pyqtSlot()
    def _opened(self): self._open=True

    def close(self): self._close.emit()

    @pyqtSlot()
    def _closed(self): self._open=False

    @pyqtSlot()
    def _threadFinished(self):
        del self._worker
        self._worker=None
        del self._thread
        self._thread=None

    @pyqtSlot(str)
    def _dataAcquired(self, data):
        self._data+=data
        self.readyRead.emit()

    @pyqtSlot(int)
    def _bytesWritten(self, bytes): self.bytesWritten.emit(bytes)

    def read(self, maxSize=-1):
        if maxSize==-1:
            data=self._data 
            self._data=""
        else:
            data=self._data[:maxSize]
            self._data=self._data[maxSize:]
        return data

    def bytesAvailable(self): return len(self._data)>0

    def canReadLine(self): return '\n' in self._data

    def write(self, data): self._write.emit(data)

    @staticmethod
    def ports(): return zip(*list_ports.comports())[0]

if __name__=="__main__":
    from sys import argv, exit

    class Widget(QWidget):
        def __init__(self, parent=None, **kwargs):
            QWidget.__init__(self, parent, **kwargs)

            self._serial=None

            l=QVBoxLayout(self)

            self._ports=QComboBox(self, editable=True)
            for port in aSerial.ports(): self._ports.addItem(port)
            l.addWidget(self._ports)            

            self._bauds=QComboBox(self)
            for baud in BAUDRATES: self._bauds.addItem("{0}".format(baud))
            l.addWidget(self._bauds)

            self._button=QPushButton("Start", self, clicked=self.startStopSerial)
            l.addWidget(self._button)

            self._log=QPlainTextEdit(self)
            l.addWidget(self._log)

            self._output=QLineEdit(self)
            l.addWidget(self._output)

            self._send=QPushButton("Send", self, clicked=self.sendData)
            l.addWidget(self._send)

        def startStopSerial(self):
            if self._serial and self._serial.isOpen():
                self._serial.close()
                self._button.setText("Start")
            else:
                self._serial=aSerial(
                    str(self._ports.currentText()),
                    int(self._bauds.currentText()),
                    self,
                    readyRead=self.dataAvailable,
                    bytesWritten=self.dataSent
                )
                self._serial.open(QIODevice.ReadWrite)
                self._button.setText("Stop")

        def dataAvailable(self):
            data=self._serial.read()
            self._log.setPlainText(self._log.toPlainText()+'\n'+data)

        @pyqtSlot()
        def sendData(self):
            self._serial.write(self._output.text())
            self._output.setText('')

        @pyqtSlot(int)
        def dataSent(self, bytes):
            self._log.setPlainText(self._log.toPlainText()+'{0} bytes sent\n'.format(bytes))

    a=QApplication(argv)
    w=Widget()
    w.show()
    w.raise_()
    exit(a.exec_())