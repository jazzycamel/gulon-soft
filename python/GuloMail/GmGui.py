from PyQt4.QtGui import QMainWindow, QIcon, QAction, QKeySequence, QMessageBox, QSplitter
from PyQt4.QtCore import QString, QChar
from GmCore import *

class GmApp(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__() 

        self.setWindowTitle("GuloMail by GulonSoft")
        self.setWindowIcon(QIcon("g-square.png"))

        self.createActions()
        self.createStatusBar()
        self.createMenus()
        self.createToolbars()
        self.createLayouts()

    def createActions(self):
        self.newAction=QAction("&New", self, shortcut=QKeySequence.New, statusTip="New")
        self.sendReceiveAction=QAction("Send / &Receive", self, shortcut="F9", statusTip="Send / Receive")
        self.printAction=QAction("&Print...", self, shortcut="Ctrl+P", statusTip="Print")
        self.quitAction=QAction("&Quit", self, shortcut="Ctrl+Q", statusTip="Quit", triggered=self.close) 

        self.copyAction=QAction("&Copy", self, statusTip="Copy", shortcut=QKeySequence.Copy)
        self.deleteAction=QAction("&Delete", self, statusTip="Delete Message")

        self.nextAction=QAction("Next &Unread Message", self, shortcut="Ctrl+]", statusTip="Next unread message")
        self.previousAction=QAction("P&revious Unread Message", self, shortcut="Ctrl+[", statusTip="Previous unread message")
        self.replyAction=QAction("&Reply", self, shortcut="Ctrl+R", statusTip="Reply to sender", triggered=self.reply)
        self.replyToAllAction=QAction("Reply to &All", self, shortcut="Ctrl+Shift+R", statusTip="Reply to all", triggered=self.replyToAll)
        self.forwardAction=QAction("&Forward", self, shortcut="Ctrl+F", statusTip="Forward")
        self.junkAction=QAction("Junk", self, shortcut="Ctrl+J", statusTip="Mark as Junk")
        self.notJunkAction=QAction("Not junk", self, shortcut="Shift+Ctrl+J", statusTip="Mark as Not Junk")

        self.contentsAction=QAction("&Contents", self, statusTip="Help Contents", shortcut="F1", triggered=self.helpContents)
        self.aboutAction=QAction("&About", self, statusTip="About GuloMail", triggered=self.about)

        self.cancelAction=QAction("&Cancel", self, statusTip="Cancel")

    def createStatusBar(self):
        self.statusBar()
        
    def createMenus(self):
        self.fileMenu=self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.sendReceiveAction)
        self.fileMenu.addAction(self.printAction)
        self.fileMenu.addAction(self.quitAction)

        self.editMenu=self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.deleteAction)

        self.viewMenu=self.menuBar().addMenu("&View")
        self.folderMenu=self.menuBar().addMenu("F&older")

        self.messageMenu=self.menuBar().addMenu("&Message")
        self.goToMenu=self.messageMenu.addMenu("&Go To")
        self.goToMenu.addAction(self.nextAction)
        self.goToMenu.addAction(self.previousAction)
        self.messageMenu.addAction(self.replyAction)
        self.messageMenu.addAction(self.replyToAllAction)
        self.messageMenu.addAction(self.forwardAction)
        self.markAsMenu=self.messageMenu.addMenu("Mar&k as...")
        self.markAsMenu.addAction(self.junkAction)
        self.markAsMenu.addAction(self.notJunkAction)

        self.searchMenu=self.menuBar().addMenu("&Search")
        
        self.helpMenu=self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.contentsAction)
        self.helpMenu.addAction(self.aboutAction)

    def createToolbars(self):
        self.toolbar=self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.sendReceiveAction)
        self.toolbar.addAction(self.replyAction)
        self.toolbar.addAction(self.replyToAllAction)
        self.toolbar.addAction(self.forwardAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.deleteAction)
        self.toolbar.addAction(self.junkAction)
        self.toolbar.addAction(self.notJunkAction)
        self.toolbar.addAction(self.cancelAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.previousAction)
        self.toolbar.addAction(self.nextAction)

    def createLayouts(self):
        self.centralWidget=QSplitter()
        
        self.setCentralWidget(self.centralWidget)

    def helpContents(self):
        print "Help"

    def reply(self):
        print "Reply"

    def replyToAll(self):
        print "Reply To All"

    def about(self):
        text=QString("GuloMail v0.1\n\n")
        text.append("GuloMail is a freeware email client written in Python using PyQt4 (Python bindings for Nokia's Qt)\n\n")
        text.append(QChar(0x00A9))
        text.append("GulonSoft 2010\nhttp://www.gulon.co.uk/")
        QMessageBox.about(self, "About GuloMail", text)
