from Queue import Queue, Empty
from os import environ
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *

class Socket(QTcpSocket):
    def __init__(self):
        QTcpSocket.__init__(self)
        self.disconnected.connect(self.gone)

    def gone(self):
        print "Connection Closed..."

class Thread(QThread):
    def __init__(self, function, *argv, **kwargs):
        QThread.__init__(self)
        self.function=function
        self.argv=argv
        self.kwargs=kwargs

    def run(self):
        self.function(self, *self.argv, **self.kwargs)

class IO(object):
    def __init__(self, socket=None, queue=None, name=None, host=None, port=None):
        self.name = name or '?'
        self._socket = socket
        self._queue = queue
        self._host = host or environ.get('SERVER_HOST','')
        self._port = port or environ.get('SERVER_PORT','')
        self._working = True
        self._queue = queue or Queue()
        self.t = Thread(self._work)
        self.t.start()

    def __repr__(self):
        return self.name
    
    def put(self, *a):
        print 'put', self.name, a
        self._socket.writeData(','.join([str(x) for x in a])+';')

    def get(self):
        """
        Receive a message from the queue.
        """
        try:
            result = self._queue.get(block=False)
            print 'get', result
            return result
        except Empty, msg:
            return None

    def quit(self):
        print 'quit'
        self._working = False

    def _qput(self, *a):
        self._queue.put((self,)+a)

    def _work(self, thread):
        qput = self._qput
        s = self._socket
        if not s: # may already exist
            self._socket = s = self._connect()
            if not s:
                qput('finished_msg')
                return
        print "Started", s.state()
        qput('started_msg', self._host, self._port)
        self._socket.readyRead.connect(self._read)
        thread.exec_()

    def _read(self):
        d=self._socket.readLine().data()
        print d
        if d.endswith(';'):
            if d=='bye_msg;':
                self.put(d[:-1])
                self._socket.close()
                self._qput('finished_msg')
            else:
                self._qput(*d[:-1].split(','))

class ClientIO(IO):
    def _connect(self):
        HOST=self._host
        PORT=int(self._port)
        while self._working:
            s=Socket()
            print 'trying to connect to %s@%s' %  (HOST, PORT)
            s.connectToHost(QHostAddress(HOST),int(PORT))
            if not s.waitForConnected(5000):
                print 'Failed to connect, error code:', s.error()
                s.close()
                return None
            else:
                self._host = HOST
                print 'connected to %s@%s' %  (HOST, PORT)
                print s.state()
                return s

class Server(QTcpServer):
    def __init__(self, handler):
        QTcpServer.__init__(self)
        self.handler=handler
        print "server"

    def incomingConnection(self, socketDescription):
        self.handler(socketDescription)

class ServerIO(IO):
    def _work(self, thread):
        """
        A servers job is to start client threads as they arrive.
        Clients have a ready made socket and queue.
        """
        server=Server(self._incoming)
        print "Listening..."
        if not server.listen(QHostAddress(self._host),int(self._port)):
            print "ERROR!"
        thread.exec_()

    def _incoming(self, socketDescriptor):
        clientsocket=Socket()
        clientsocket.setSocketDescriptor(socketDescriptor)
        IO(clientsocket, self._queue)
