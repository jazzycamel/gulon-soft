from sys import argv, exit
from PyQt4.QtCore import *
from PyQt4.QtXml import *
from PyQt4.QtGui import *

# domitem.cpp/.h
class DomItem:
    def __init__(self, node, row, parent=None):
        self.domNode=node
        self.rowNumber=row
        self.parentItem=parent
        self.childItems={}

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    def child(self, i):
        if self.childItems.has_key(i): 
            return self.childItems[i]

        if i>=0 and i<self.domNode.childNodes().count():
            childNode=self.domNode.childNodes().item(i)
            childItem=DomItem(childNode, i, self)
            self.childItems[i]=childItem
            return childItem

        return 0

    def row(self):
        return self.rowNumber

# dommodel.cpp/.h
class DomModel(QAbstractItemModel):
    def __init__(self, document, parent=None):
        QAbstractItemModel.__init__(self, parent)

        self.domDocument=document
        self.rootItem=DomItem(self.domDocument,0)

    def columnCount(self, parentIndex):
        return 3

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if not role==Qt.DisplayRole:
            return QVariant()

        item=index.internalPointer()
        node=item.node()
        attributes=QStringList()
        attributeMap=node.attributes()

        column=index.column()
        if column==0: return QVariant(node.nodeName())
        elif column==1:
            for i in range(0,attributeMap.count()):
                attribute=attributeMap.item(i)
                attributes.append(attribute.nodeName() + "=\"" + attribute.nodeValue() + "\"")
            return QVariant(attributes.join(" "))
        elif column==2: return QVariant(node.nodeValue().split("\n").join(" "))
        else: return QVariant()

    def flags(self, index):
        if not index.isValid(): return Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
  
    def headerData(self, section, orientation, role):
        if orientation==Qt.Horizontal and role==Qt.DisplayRole:
            if section==0: return QVariant("Name")
            elif section==1: return QVariant("Attributes")
            elif section==2: return QVariant("Value")
            else: return QVariant()
        return QVariant()

    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):return QModelIndex()
        #if not self.hasIndex(row, column, parent): return QModelIndex()

        if not parent.isValid(): parentItem=self.rootItem
        else: parentItem=parent.internalPointer()

        childItem=parentItem.child(row)
        if childItem: return self.createIndex(row, column, childItem)
        else: return QModelIndex()

    def parent(self, child):
        if not child.isValid(): return QModelIndex()
        
        childItem=child.internalPointer()
        parentItem=childItem.parent()

        if not parentItem or parentItem==self.rootItem: return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0: return 0
         
        if not parent.isValid(): parentItem=self.rootItem
        else: parentItem=parent.internalPointer()

        return parentItem.node().childNodes().count()

# mainwindow.cpp/.h
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.fileMenu=fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(QAction("&Open...", self, triggered=self.openFile, shortcut=QKeySequence.Open))
        fileMenu.addAction(QAction("E&xit", self, triggered=self.close, shortcut=QKeySequence.Quit))

        self.xmlPath=''
        self.model=model = DomModel(QDomDocument(), self)
        self.view=view = QTreeView(self)
        view.setModel(model)

        self.setCentralWidget(view)
        self.setWindowTitle("Simple DOM Model")

    def openFile(self):
        filePath = QFileDialog.getOpenFileName(self, "Open File", self.xmlPath, "XML files (*.xml);;HTML files (*.html);; SVG files (*.svg);;User Interface files (*.ui)")

        if not filePath.isEmpty():
            _file=QFile(filePath)
            if _file.open(QIODevice.ReadOnly):
                document=QDomDocument()
                if document.setContent(_file):
                    newModel = DomModel(document, self)
                    self.view.setModel(newModel);
                    self.model = newModel
                    self.xmlPath = filePath
                _file.close()

# main.cpp
if __name__=="__main__":
    a=QApplication(argv)
    window=MainWindow()
    window.resize(640,480)
    window.show()
    exit(a.exec_())
