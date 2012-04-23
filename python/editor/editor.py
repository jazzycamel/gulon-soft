from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

class LexerStyle(object):
    def __init__(self, _color=None, _paper=None, _font=""):
        self.color=QColor(_color)
        self.font=QFont("Monaco", 12)
        self.paper=QColor(_paper)

class ZenburnTheme(object):
    def __init__(self):
        self._styles={
            "def:boolean"       : LexerStyle("#dca3a3"),
            "comment"           : LexerStyle("#7f9f7f"),             #italic
            "def:constant"      : LexerStyle("#dca3a3"),             #bold
            "cursor"            : LexerStyle("#000d18", "#8faf9f") , #bold
            "diff:added_line"   : LexerStyle("#709080", "#313c36"),  #bold
            "diff:changed-line" : LexerStyle("", "#333333"),
            "diff:removed-line" : LexerStyle("#333333", "#464646"),
            "def:function"      : LexerStyle("#efef8f", ""),
            "def:identifier"    : LexerStyle("#efdcbc", ""),
            "def:keyword"       : LexerStyle("#f0dfaf", ""),         #bold
            "def:number"        : LexerStyle("#8cd0d3", ""),
            "def:preprocessor"  : LexerStyle("#ffcfaf", ""),         #bold
            "search-match"      : LexerStyle("#ffffe0", "#284f28"),
            "def:specials"      : LexerStyle("#cfbfaf", ""),
            "def:statement"     : LexerStyle("#e3ceab", ""),
            "def:string"        : LexerStyle("#cc9393", ""),
            "def:type"          : LexerStyle("#dfdfbf", ""),         #bold
            "def:error"         : LexerStyle("#e37170", "#3d3535"),
            "text"              : LexerStyle("#dcdccc", "#3f3f3f"),
            "current-line"      : LexerStyle("", "#434443"),
            "bracket-match"     : LexerStyle("#b2b2a0", "#2e2e2e"),  #bold
            "line-numbers"      : LexerStyle("#9fafaf", "#262626"),
        }

class BaseLexer(object):
    def __init__(self):
        self.theme=ZenburnTheme()
        #self.__styles={}
        print self.keywords
        

    def styleNames(self): return self._styles.keys()

    def paper(self, style): 
        color = self.theme._styles[ self.styles(style) ].paper if self.styles(style) else self.defaultPaper(style)
        return color if color.isValid() else QColor("#3f3f3f")

    def color(self, style):
        return self.theme._styles[ self.styles(style) ].color if self.styles(style) else self.defaultColor(style)

    def font(self, style):
        return self.theme._styles[ self.styles(style) ].font if self.styles(style) else self.defaultFont(style)

from inspect import getmro

class PythonLexer(BaseLexer, QsciLexerPython):
    _styles={
        "Default"                  : QsciLexerPython.Default,
        "Comment"                  : QsciLexerPython.Comment,
        "Number"                   : QsciLexerPython.Number,
        "DoubleQuotedString"       : QsciLexerPython.DoubleQuotedString,
        "SingleQuotedString"       : QsciLexerPython.SingleQuotedString,
        "Keyword"                  : QsciLexerPython.Keyword,
        "TripleSingleQuotedString" : QsciLexerPython.TripleSingleQuotedString,
        "TripleDoubleQuotedString" : QsciLexerPython.TripleDoubleQuotedString,
        "ClassName"                : QsciLexerPython.ClassName,
        "FunctionMethodName"       : QsciLexerPython.FunctionMethodName,
        "Operator"                 : QsciLexerPython.Operator,
        "Identifier"               : QsciLexerPython.Identifier,
        "CommentBlock"             : QsciLexerPython.CommentBlock,
        "UnclosedString"           : QsciLexerPython.UnclosedString,
        "HighlightedIdentifier"    : QsciLexerPython.HighlightedIdentifier,
        "Decorator"                : QsciLexerPython.Decorator,
    }

    def __init__(self, parent=None):
        self.__styles={
            QsciLexerPython.Default                  : "text",
            QsciLexerPython.Comment                  : "comment",
            QsciLexerPython.Number                   : "def:number",
            QsciLexerPython.DoubleQuotedString       : "def:string",
            QsciLexerPython.SingleQuotedString       : "def:string",
            QsciLexerPython.Keyword                  : "def:keyword",
            QsciLexerPython.TripleSingleQuotedString : "def:string",
            QsciLexerPython.TripleDoubleQuotedString : "def:string",
            QsciLexerPython.ClassName                : "def:function",
            QsciLexerPython.FunctionMethodName       : "def:function",
            QsciLexerPython.Operator                 : "def:specials",
            QsciLexerPython.Identifier               : "text",
            QsciLexerPython.CommentBlock             : "comment",
            QsciLexerPython.UnclosedString           : "def:error",
            QsciLexerPython.HighlightedIdentifier    : "text",
            QsciLexerPython.Decorator                : "def:specials",
        }

        BaseLexer.__init__(self)
        QsciLexerPython.__init__(self, parent)

    def keywords(self, _set):
        kw=QsciLexerPython.keywords(self, _set)
        return (kw+' self') if kw else kw

    def styles(self, style): return self.__styles[style] if self.__styles.has_key(style) else None

    def defaultPaper(self, style): return QColor("#3f3f3f")
    
class Editor(QsciScintilla):
    ARROW_MARKER_NUM=8

    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)

        font=QFont()
        font.setFamily('courier')
        font.setFixedPitch(True)
        font.setPointSize(14)
        self.setFont(font)
        self.setMarginsFont(font)

        fontMetrics=QFontMetrics(font)
        self.setMarginWidth(0, fontMetrics.width("00000")+6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor('#CCCCCC'))
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.onMarginClicked)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#EE1111"), self.ARROW_MARKER_NUM)

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        lexer=PythonLexer()
        print lexer.styleNames()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        self.setMinimumSize(600,450)

    def onMarginClicked(self, margin, nline, modifiers):
        if self.markersAtLine(nline)!=0: self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else: self.markersAdd(nline, self.ARROW_MARKER_NUM)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.textEdit=Editor(self)
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.textEdit.textChanged.connect(self.documentWasModified)

        self.setCurrentFile("")

    def closeEvent(self, e):
        if self.maybeSave():
            self.writeSettings()
            e.accept()
        else: e.ignore()

    def newFile(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile("")

    def openFile(self):
        if self.maybeSave():
            fileName=QFileDialog.getOpenFileName(self)
            if not fileName.isEmpty(): self.loadFile(fileName)

    def save(self):
        if self.curFile.isEmpty(): return self.saveAs()
        else: return self.saveFile(self.curFile)

    def saveAs(self):
        fileName=QFileDialog.getSaveFileName(self)
        if fileName.isEmpty(): return False
        return self.saveFile(fileName)

    def about(self):
        QMessageBox.about(self,
                          "About Application",
                          "The <b>Application</b> examples demonstrates how to "\
                          "write modern GUI applications using Qt, with a menu bar, "\
                          "toolbars, and a status bar.")

    def documentWasModified(self): self.setWindowModified(self.textEdit.isModified())

    def createActions(self):
        self.newAct=QAction(QIcon('./images/new.png'), "&New", self, shortcut="Ctrl+N")
        self.newAct.setStatusTip("Create a new file")
        self.newAct.triggered.connect(self.newFile)

        self.openAct=QAction(QIcon('./images/open.png'), "&Open...", self, shortcut="Ctrl+O")
        self.openAct.setStatusTip("Open an existing file")
        self.openAct.triggered.connect(self.openFile)

        self.saveAct=QAction(QIcon('./images/save.png'), "&Save", self, shortcut="Ctrl+S")
        self.saveAct.setStatusTip("Save the document to disk")
        self.saveAct.triggered.connect(self.save)

        self.saveAsAct=QAction(QIcon('./images/save.png'), "Save &As...", self)
        self.saveAsAct.setStatusTip("Save the document under a new name")
        self.saveAsAct.triggered.connect(self.save)

        self.exitAct=QAction("E&xit", self, shortcut="Ctrl+Q")
        self.exitAct.setStatusTip("Exit the application")
        self.exitAct.triggered.connect(self.close)

        self.cutAct=QAction(QIcon("./images/cut.png"), "Cu&t", self, shortcut="Ctrl+X")
        self.cutAct.setStatusTip("Cut the current selection's contents to the clipboard")
        self.cutAct.triggered.connect(self.textEdit.cut)
        self.cutAct.setEnabled(False)
        self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)

        self.copyAct=QAction(QIcon("./images/copy.png"), "&Copy", self, shortcut="Ctrl+C")
        self.copyAct.setStatusTip("Copy the current selection's contents to the clipboard")
        self.copyAct.triggered.connect(self.textEdit.copy)
        self.copyAct.setEnabled(False)
        self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

        self.pasteAct=QAction(QIcon("./images/paste.png"), "&Paste", self, shortcut="Ctrl+V")
        self.pasteAct.setStatusTip("Paste the clipboard's contents into the current selection")
        self.pasteAct.triggered.connect(self.textEdit.paste)

        self.aboutAct=QAction("&About", self)
        self.aboutAct.setStatusTip("Show the application's About box")
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct=QAction("About &Qt", self)
        self.aboutQtAct.setStatusTip("Show the Qt Library's About box")
        self.aboutQtAct.triggered.connect(QApplication.aboutQt)

    def createMenus(self):
        fileMenu=self.menuBar().addMenu("&File")
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addAction(self.exitAct)

        editMenu=self.menuBar().addMenu("&Edit")
        editMenu.addAction(self.cutAct)
        editMenu.addAction(self.copyAct)
        editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        helpMenu=self.menuBar().addMenu("&Help")
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        fileToolBar=self.addToolBar("File")
        fileToolBar.addAction(self.newAct)
        fileToolBar.addAction(self.openAct)
        fileToolBar.addAction(self.saveAct)

        editToolBar=self.addToolBar("Edit")
        editToolBar.addAction(self.cutAct)
        editToolBar.addAction(self.copyAct)
        editToolBar.addAction(self.pasteAct)

    def createStatusBar(self): self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings=QSettings("GulonSoft", "QScintilla Exmaple")
        pos=settings.value("pos", QPoint(200,200)).toPoint()
        size=settings.value("size", QSize(400,400)).toSize()
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings=QSettings("GulonSoft", "QScintilla Exmaple")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        if not self.textEdit.isModified(): return True
        ret=QMessageBox.warning(self,
                                "Application",
                                "The document has been modified.\n"\
                                "Do you want to save your changes?",
                                QMessageBox.Yes | QMessageBox.Default,
                                QMessageBox.No,
                                QMessageBox.Cancel | QMessageBox.Escape)
        if ret==QMessageBox.Yes: return self.save()
        elif ret==QMessageBox.Cancel: return False
        else: return True

    def loadFile(self, fileName):
        _file=QFile(fileName)
        if not _file.open(QFile.ReadOnly):
            QMessageBox.warning(self,
                                "Application",
                                "Cannot read file %s:\n%s" % (fileName, str(_file.errorString())))
            return
        _in=QTextStream(_file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setText(_in.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        _file=QFile(fileName)
        if not _file.open(QFile.ReadOnly):
            QMessageBox.warning(self, 
                                "Application",
                                "Cannot write file %d:\n%2" % (fileName, str(_file.errorString())))
            return False
        _out=QTextStream(_file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        _out << self.textEdit.text()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
    
    def setCurrentFile(self, fileName):
        self.curFile=fileName
        self.textEdit.setModified(False)
        self.setWindowModified(False)

        shownName="untitled.txt" if len(self.curFile)==0 else self.strippedName(self.curFile)
        self.setWindowTitle("%s[*] - Application" % shownName)

    def strippedName(self, fullFileName): return QFileInfo(fullFileName).fileName()

if __name__=="__main__":
    from sys import argv, exit
    a=QApplication(argv)
    m=MainWindow()
    m.show()
    exit(a.exec_())
