from sys import argv
from PyQt4.QtGui import *
from IO import ServerIO
from IOGui import IOGui, message

class ServerGUI(IOGui):
    def create_widgets(self):
        pass

    @message
    def hi_msg(self, client, name):
        client.name=name

if __name__=='__main__':
    a=QApplication(argv)
    s=ServerGUI(ServerIO())
    s.show()
    a.exec_()
