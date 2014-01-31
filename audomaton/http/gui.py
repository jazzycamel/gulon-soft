import sip
sip.setapi('QString',2)
sip.setapi('QVariant',2)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from httpserver import HttpServer

class ServerGui(QWidget):
    def __init__(self, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)

        self.setWindowTitle("Server")

        self._running=False
        self._server=HttpServer(self)

        l=QGridLayout(self)
        l.addWidget(QPushButton("Start", self, checkable=True, clicked=self.startStop), 0, 0)

        sgb=QGroupBox("Settings", self)
        sl=QFormLayout(sgb)
        l.addWidget(sgb, 1, 0)

        self._host=QLineEdit('127.0.0.1', self)
        sl.addRow("Host:", self._host)

        self._port=QSpinBox(self, value=8080, minimum=1024, maximum=99999)
        sl.addRow("Port:", self._port)

        rdl=QHBoxLayout()
        rdl.setContentsMargins(0,0,0,0)
        self._rootDir=QLineEdit(QDir('./www').absolutePath(), self)
        rdl.addWidget(self._rootDir)
        rdl.addWidget(QPushButton("Browse...", self, clicked=self.setRootDir))
        sl.addRow("Root Directory:", rdl)

    @pyqtSlot()
    def startStop(self):
        self._running=self.sender().isChecked()

        self.sender().setText('Stop' if self._running else 'Start')

        if self._running:
            self._server.start(
                self._host.text(),
                self._port.value(),
                self._rootDir.text()
            )
        else: self._server.stop()

    @pyqtSlot()
    def setRootDir(self):
        current=self._rootDir.text()
        root=QFileDialog.getExistingDirectory(self, 'Select Root Directory...', current)

        if not root: return
        self._rootDir.setText(root)

if __name__=='__main__':
    from sys import argv, exit

    a=QApplication(argv)
    s=ServerGui()
    s.show()
    s.raise_()
    exit(a.exec_())