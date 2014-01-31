from PyQt4.QtCore import *
from PyQt4.QtNetwork import *
import os

from parser import HttpParser
from util import status_reasons

ext2ct={
    'html': 'text/html; charset="utf8"',
    'css' : 'text/css',
    'js'  : 'application/javascript',
    'png' : 'image/png',
    'jpg' : 'image/jpeg',
    'gif' : 'image/gif',
}

RESPONSE  = 'HTTP/1.0 {code} {status}\r\n'
RESPONSE += 'Server: HttpServer\r\n'
RESPONSE += 'Connection: close\r\n'
RESPONSE += 'Content-Type: {content-type}\r\n'
RESPONSE += '\r\n'
RESPONSE += '{content}'
RESPONSE += '\n'

class Error404(Exception): pass

class HttpServer(QTcpServer):
    def __init__(self, parent=None, **kwargs):
        QTcpServer.__init__(self, parent, **kwargs)

        self._sockets=[]

    def incomingConnection(self, handle):
        if not self.isListening(): return

        s=QTcpSocket(self, readyRead=self.readClient, disconnected=self.discardClient)
        s.setSocketDescriptor(handle)
        self._sockets.append(s)

    def start(self, host=QHostAddress.LocalHost, port=8080, root='.'):
        self._root=root
        return self.listen(QHostAddress(host),port)

    def stop(self):
        if self.isListening(): self.close()

    def readClient(self):
        s=self.sender()
        headers=str(s.readAll())

        p=HttpParser()
        plen=p.execute(headers, len(headers))

        if p.get_method()=="GET":
            path=p.get_path()

            try:
                _path=os.path.join(self._root, path[1:])
                if not os.path.exists(_path): raise Error404
                elif os.path.isdir(_path):
                    _path=os.path.join(_path, 'index.html')
                    if not os.path.exists(_path): raise Error404

                ext=os.path.splitext(_path)[1][1:].lower()
                code=200
                with open(_path, 'rb') as f: content=f.read()

            except Error404 as e:
                code=404
                ext='html'
                content='<h1>404 - File Not Found ({0})</h1>'.format(path)

            except Exception as e:
                code=500
                ext='html'
                content='<h1>500 - Internal Error</h1>'

            _resp={
                'code'         : code,
                'status'       : status_reasons[code],
                'content-type' : ext2ct[ext],
                'content'      : content
            }

            response=RESPONSE.format(**_resp)

        elif p.get_method()=='POST':
            print "POST", headers
            response=''

        else: response=''
        
        s.writeData(response)
        s.waitForBytesWritten()
        s.close()

    def discardClient(self):
        s=self.sender()
        self._sockets.remove(s)
        s.deleteLater()