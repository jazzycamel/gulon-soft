from PyQt4.QtCore import *
from PyQt4.QtGui import *

_ROLES={
    "Window"          : QPalette.Window,
    "WindowText"      : QPalette.WindowText,
    "Base"            : QPalette.Base,
    "AlternateBase"   : QPalette.AlternateBase,
    "Text"            : QPalette.Text,
    "Button"          : QPalette.Button,
    "ButtonText"      : QPalette.ButtonText,
    "BrightText"      : QPalette.BrightText,
    "Light"           : QPalette.Light,
    "Midlight"        : QPalette.Midlight,
    "Dark"            : QPalette.Dark,
    "Mid"             : QPalette.Mid,
    "Shadow"          : QPalette.Shadow,
    "Highlight"       : QPalette.Highlight,
    "HighlightedText" : QPalette.HighlightedText,
    "Link"            : QPalette.Link,
    "LinkVisited"     : QPalette.LinkVisited
}

_GROUPS={
    "Active"   : QPalette.Active,
    "Inactive" : QPalette.Inactive,
    "Disabled" : QPalette.Disabled
}

class PaletteViewer(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

        self.setSelectionMode(QTableWidget.NoSelection)
        self.setSortingEnabled(False)
        self.verticalHeader().hide()
        self.setRowCount(len(_ROLES))
        self.setColumnCount(len(_GROUPS)+1)
        self.setHorizontalHeaderLabels(['Role']+_GROUPS.keys())
        self.setFrameStyle(QFrame.NoFrame)

        palette=self.palette()

        for r, (name, role) in enumerate(_ROLES.iteritems()):
            self.setItem(r, 0, QTableWidgetItem(name))
            for g, (groupName, group) in enumerate(_GROUPS.iteritems()):
                color=palette.color(group, role)
                pixmap=QPixmap(32,32)
                painter=QPainter()
                painter.begin(pixmap)
                painter.fillRect(pixmap.rect(), Qt.black)
                painter.fillRect(pixmap.rect().adjusted(1,1,-1,-1), color)
                painter.end()
                rgb="%03d %03d %03d" % (color.red(), color.green(), color.blue())
                self.setItem(r, g+1, QTableWidgetItem(QIcon(pixmap), rgb))


        self.setWindowTitle("Palette Viewer")
        self.resizeColumnsToContents()
        self.horizontalHeader().setResizeMode(0,QHeaderView.Stretch)

        self.resize(640,540)

if __name__=="__main__":
    from sys import argv, exit
    a=QApplication(argv)
    p=PaletteViewer()
    p.show()
    p.raise_()
    exit(a.exec_())
