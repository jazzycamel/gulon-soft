from sys import argv
from PyQt4.QtGui import *
from IO import ClientIO
from IOGui import IOGui, message

NAME='Client'

class ClientGUI(IOGui):
    def create_widgets(self):
        pass

    @message
    def started_msg(self, sender, host, port):
        self.put=sender.put
        self.put('hi_msg', NAME)

if __name__=='__main__':
    a=QApplication(argv)
    c=ClientGUI(ClientIO())
    c.show()
    a.exec_()
