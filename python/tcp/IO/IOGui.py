from functools import wraps
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def message(method):
    """
    Decorator for message methods.
    Add the message into the list of expected messages.
    """
    message.messages.add(method.__name__)
    @wraps(method)
    def decorated(self, sender, *args):
        method(self, sender, *args)
    return decorated
message.messages = set()

class IOGui(QMainWindow):
    def __init__(self, io):
        QMainWindow.__init__(self)

        self._pending_quit=False
        self._io=io
        self.create_widgets()
        self._suspend()

    def _delete_window(self):
        if self._pending_quit:
            self._cleanup()
        else:
            self._pending_quit = True
            self._io.quit()

    def _cleanup(self):
        if self._suspended:
            """ Connect to quit? """
            pass
            #self._root.after_cancel(self._suspended)
        self.quit()

    def _suspend(self):
        self._suspended = QTimer.singleShot(20, self._check_io)

    def _check_io(self):
        """
        read all messages from io and pass on as methods
        """
        self._suspended = None
        while True:
            data = self._io.get()
            if not data:
                self._suspend()
                return
            sender = data[0]
            method = data[1]
            if method in message.messages:
                getattr(self, method)(sender, *data[2:])
            else:
                print 'missing method for message', data

    @message
    def error_msg(self, sender, msg):
        """
        Called to report errors.
        """
        print 'roll your own error_msg handler', sender, msg

    @message
    def started_msg(self, sender, host, port):
        """
        Called whenever a connection is made.
        """
        print 'roll your own started_msg handler', sender, host, port

    @message
    def bye_msg(self, sender):
        """
        Called just before a connection is broken.
        """
        print 'roll your own bye_msg handler', sender

    @message
    def finished_msg(self, sender):
        """
        Called whenever a connection is broken.
        If you roll your own be sure to call this one when all is done.
        """
        self._cleanup()
