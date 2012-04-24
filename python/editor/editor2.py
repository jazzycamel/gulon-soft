from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
Q_WS_MAC=Q_OS_MAC=sys.platform=='darwin'

class Editor(QTextEdit):
    """This will be a QsciScintilla when I get around to it"""
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle("%s %s" % (QApplication.applicationName(), QApplication.applicationVersion()))
        self.setWindowIcon(QIcon("./icons/gulon.png"))

        self.openDocuments=[]

        self.createActions()
        self.statusBar()
        self.createToolBar()
        self.createMenu()
        self.createWidgets()

    def createActions(self):
        # File Actions
        self.newAction=QAction(QIcon.fromTheme("document-new", QIcon("./icons/page.png")), "&New", self, shortcut="Ctrl+N", triggered=self.addNewDocument)
        self.newAction.setStatusTip("Create a new document")

        self.openAction=QAction(QIcon.fromTheme("document-open", QIcon("./icons/folder.png")), "&Open...", self, shortcut="Ctrl+O")
        self.openAction.setStatusTip("Open a file")

        self.saveAction=QAction(QIcon.fromTheme("document-save", QIcon("./icons/disk.png")), "&Save", self, shortcut="Ctrl+S")
        self.saveAction.setStatusTip("Save the current file")

        self.saveAsAction=QAction(QIcon.fromTheme("document-save-as"), "Save As...", self, shortcut="Shift+Ctrl+S")
        self.saveAsAction.setStatusTip("Save a copy of the current file...")

        self.printAction=QAction(QIcon.fromTheme("document-print", QIcon("./icons/printer.png")), "&Print...", self, shortcut="Ctrl+P")
        self.printAction.setStatusTip("Print the current page")

        self.quitAction=QAction(QIcon.fromTheme("application-exit", QIcon("./door_out.png")), "&Quit", self, shortcut="Ctrl+Q", triggered=self.close)

        # Edit Actions
        self.undoAction=QAction(QIcon.fromTheme("edit-undo", QIcon("./icons/arrow_undo.png")), "&Undo", self, shortcut="Ctrl+Z")
        self.undoAction.setStatusTip("Undo the last action")

        self.redoAction=QAction(QIcon.fromTheme("edit-redo", QIcon("./icons/arrow_redo.png")), "&Redo", self, shortcut="Shift+Ctrl+Z")
        self.redoAction.setStatusTip("Redo the last undone action")
        self.redoAction.setEnabled(False)

        self.cutAction=QAction(QIcon.fromTheme("edit-cut", QIcon("./icons/cut.png")), "Cut", self, shortcut="Ctrl+X")
        self.cutAction.setStatusTip("Cut the selection")
        self.cutAction.setEnabled(False)

        self.copyAction=QAction(QIcon.fromTheme("edit-copy", QIcon("./icons/page_copy.png")), "&Copy", self, shortcut="Ctrl+C")
        self.copyAction.setStatusTip("Copy the selection")
        self.copyAction.setEnabled(False)

        self.pasteAction=QAction(QIcon.fromTheme("edit-paste", QIcon("./icons/page_paste.png")), "&Paste", self, shortcut="Ctrl+V")
        self.pasteAction.setStatusTip("Paste the clipboard")

        self.selectAllAction=QAction(QIcon.fromTheme("edit-select-all"), "Select All", self, shortcut="Ctrl+A")
        self.selectAllAction.setStatusTip("Select all contents of the current file")

        # Search Actions
        self.findAction=QAction(QIcon.fromTheme("edit-find", QIcon("./icons/find.png")), "&Find...", self, shortcut="Ctrl+F")
        self.findAction.setStatusTip("Search for text")

        # Help Actions
        self.aboutAction=QAction(QIcon.fromTheme("help-about", QIcon()), "About", self, shortcut="F1", triggered=self.about)
        self.aboutQtAction=QAction(QIcon.fromTheme("help-about", QIcon()), "About Qt", self, triggered=self.aboutQt)
        self.contentsAction=QAction(QIcon.fromTheme("help-contents", QIcon()), "Contents", self)

    def createToolBar(self):
        self.toolBar=self.addToolBar("Main ToolBar")
        self.toolBar.setIconSize(QSize(16, 16))

        self.toolBar.addAction(self.newAction)
        self.toolBar.addAction(self.openAction)
        self.toolBar.addAction(self.saveAction)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.printAction)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.undoAction)
        self.toolBar.addAction(self.redoAction)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.cutAction)
        self.toolBar.addAction(self.copyAction)
        self.toolBar.addAction(self.pasteAction)

        self.toolBar.addSeparator()

        self.toolBar.addAction(self.findAction)

    def createMenu(self):
        # File Menu
        self.fileMenu=self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)

        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)

        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.printAction)

        self.fileMenu.addSeparator()

        self.fileMenu.addAction(self.quitAction)

        # Edit Menu
        self.editMenu=self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)

        self.editMenu.addSeparator()
 
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)

        self.editMenu.addSeparator()

        self.editMenu.addAction(self.selectAllAction)

        # Search Menu
        self.searchMenu=self.menuBar().addMenu("&Search")
        self.searchMenu.addAction(self.findAction)

        # Help Menu
        self.helpMenu=self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)
        self.helpMenu.addAction(self.contentsAction)

    def createWidgets(self):
        self.tabWidget=QTabWidget(self)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)

        QShortcut(QKeySequence(Qt.ALT+Qt.Key_Tab if Q_OS_MAC else QKeySequence.NextChild), self.tabWidget, lambda: self.changeTab(1))
        QShortcut(QKeySequence(Qt.ALT+Qt.SHIFT+Qt.Key_Tab if Q_OS_MAC else QKeySequence.PreviousChild), self.tabWidget, lambda: self.changeTab(-1))

        self.setCentralWidget(self.tabWidget) # This will change to a QSplitter when we get that far!

    def about(self):
        aboutText="<h1>%s %s</h1>" \
                  "<p>A lightweight editor created with PyQt4 and QScintilla</p>" \
                  "<p>%s<br /><a href=\"%s\">%s</a></p>" \
                  "<p>All icons used in this software (with the exception of the GulonSoft \"G\") are derived" \
                  " from the operating system or come from the excellent Silk theme from FamFamFam" \
                  " (<a href=\"http://www.famfamfam.com/lab/icons/silk/\">http://www.famfamfam.com/lab/icons/silk/</a>)</p>" \
                  "<p>&copy; GulonSoft 2012</p>" \
                      % (QApplication.applicationName(), 
                         QApplication.applicationVersion(), 
                         QApplication.organizationName(),
                         QApplication.organizationDomain(),
                         QApplication.organizationDomain())
    
        QMessageBox.about(self, QApplication.applicationName(), aboutText)

    def aboutQt(self): QMessageBox.aboutQt(self, "About Qt")

    def addNewDocument(self):
        document=Editor(self)
        self.tabWidget.addTab(document, "Untitled.txt")
        self.openDocuments.append(document)

    def changeTab(self, direction):
        count=self.tabWidget.count()
        if count<2: return

        current=self.tabWidget.currentIndex()
        new=current+direction
        if new<0: new+=count
        elif new>=count: new-=count

        self.tabWidget.setCurrentIndex(new)

if __name__=="__main__":
    from sys import argv, exit

    a=QApplication(argv)
    a.setOrganizationName("GulonSoft")
    a.setOrganizationDomain("http://www.gulon.co.uk/")
    a.setApplicationName("Editor")
    a.setApplicationVersion("0.1 Alpha")

    m=MainWindow()
    m.show()

    exit(a.exec_())
