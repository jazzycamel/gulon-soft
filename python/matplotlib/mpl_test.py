from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavToolbar
from matplotlib.figure import Figure
from matplotlib.colors import rgb2hex
from pylab import *

FILE_FORMATS={
  "Encapsulated Postscript"   : ['eps'],
  "Enhanced Metafile"         : ['emf'],
  "Portable Document Format"  : ['pdf'],
  "Portable Network Graphics" : ['png'],
  "Raw RGBA Bitmap"           : ['raw', 'rgba'],
  "Scalable Vector Graphics"  : ['svg', 'svgz'],                    
}

FILE_FORMATS_STR=";;".join(["%s (%s)" % (f, " ".join(["*.%s" % _e for _e in e])) for f,e in FILE_FORMATS.iteritems()])

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle("PyQt & matplotlib Test")

        self.createActions()
        self.createMenus()
        self.createMainFrame()
        self.createStatusBar()

        self.onDraw()

    def createActions(self):
        self.saveFileAction=QAction("&Save Plot", self, shortcut="Ctrl+S", triggered=self.savePlot, toolTip="Save the plot")
        self.quitAction=QAction("&Quit", self, shortcut="Ctrl+Q", triggered=self.close, toolTip="Close the application")
        self.aboutAction=QAction("&About", self, shortcut="F1", triggered=self.onAbout, toolTip="About this test")

    def createMenus(self):
        self.fileMenu=self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.saveFileAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)

        self.helpMenu=self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)

    def createMainFrame(self):
        mainWidget=QWidget(self)
        QVBoxLayout(mainWidget)

        # matplotlib widget setup
        self.figure=Figure((5.0, 4.0), dpi=100)
        self.canvas=FigureCanvas(self.figure)
        self.canvas.setParent(mainWidget)
        mainWidget.layout().addWidget(self.canvas)

        self.axes=self.figure.add_subplot(111)

        self.canvas.mpl_connect('pick_event', self.onPick)
        self.canvas.mpl_connect('motion_notify_event', self.onMove)

        self.mplToolbar=NavToolbar(self.canvas, mainWidget)
        mainWidget.layout().addWidget(self.mplToolbar)

        # other widget setup
        controlLayout=QHBoxLayout()        

        self.textbox=QLineEdit('1 2 3 4', editingFinished=self.onDraw, minimumWidth=200)
        controlLayout.addWidget(self.textbox, Qt.AlignVCenter)

        drawButton=QPushButton('&Draw', clicked=self.onDraw)
        controlLayout.addWidget(drawButton, Qt.AlignVCenter)

        self.showGrid=QCheckBox("Show &Grid", checked=False, stateChanged=self.onDraw)
        controlLayout.addWidget(self.showGrid, Qt.AlignVCenter)

        controlLayout.addWidget(QLabel("Bar Width (%)"), Qt.AlignVCenter)

        self.slider=QSlider(Qt.Horizontal, minimum=1, maximum=100, value=20, tracking=True, tickPosition=QSlider.TicksBothSides, valueChanged=self.onDraw)
        controlLayout.addWidget(self.slider, Qt.AlignVCenter)

        mainWidget.layout().addLayout(controlLayout)

        # test layout 1
        testLayout1=QHBoxLayout()

        testLayout1.addWidget(QLabel("x:", self))
        self.xValue=QLineEdit("0", self)
        testLayout1.addWidget(self.xValue)

        testLayout1.addWidget(QLabel("y:", self))
        self.yValue=QLineEdit("0", self)
        testLayout1.addWidget(self.yValue)

        testLayout1.addWidget(QLabel("pixels"))

        mainWidget.layout().addLayout(testLayout1)

        self.setCentralWidget(mainWidget)

        # test layout 2
        testLayout2=QHBoxLayout()

        testLayout2.addWidget(QLabel("x:", self))
        self.xdValue=QLineEdit("0", self)
        testLayout2.addWidget(self.xdValue)

        testLayout2.addWidget(QLabel("y:", self))
        self.ydValue=QLineEdit("0", self)
        testLayout2.addWidget(self.ydValue)

        testLayout2.addWidget(QLabel("data"))

        mainWidget.layout().addLayout(testLayout2)

    def createStatusBar(self):
        self.statusBar().addWidget(QLabel("This is a test"), 1)

    @pyqtSlot()
    def savePlot(self):
        path=str(QFileDialog.getSaveFileName(self, 'Save Plot...', '', FILE_FORMATS_STR))
        print "Save Path:", path
        if path: self.canvas.print_figure(path)

    @pyqtSlot()
    def onAbout(self):
        QMessageBox.about(
            self,
            "About this test",
            """
            <p>A test of using PyQt with matplotlib:</p>    
            <ul>
                <li>Use the matplotlib navigation bar</li>
                <li>Add values to the text box and press Enter (or click "Draw")</li>
                <li>Show or hide the grid</li>
                <li>Drag the slider to modify the width of the bars</li>
                <li>Save the plot to a file using the File menu</li>
                <li>Click on a bar to receive an informative message</li>
            </ul>
            """)

    def onPick(self, event):
        QMessageBox.information(
            self,
            "Click!",
            "You've clicked on a bar with coords:\n%s" % event.artist.get_bbox().get_points())

    def onMove(self, event):
        self.xValue.setText("%d" % event.x)
        self.yValue.setText("%d" % event.y)

        if event.inaxes:
            self.xdValue.setText("%f" % event.xdata)
            self.ydValue.setText("%f" % event.ydata)

    @pyqtSlot()
    def onDraw(self):
        data=map(int, str(self.textbox.text()).split())
        x=range(len(data))

        e=0.5*(randn(len(data)))

        self.axes.clear()
        self.axes.grid(self.showGrid.isChecked())
        self.axes.bar(
            left=x,
            height=data,
            width=self.slider.value()/100.0,
            align='center',
            picker=5,
            alpha=0.5)

        self.axes.errorbar(x, data, e, fmt='o', ms=0)

        self.canvas.draw()

if __name__=="__main__":
    from sys import argv, exit
    a=QApplication(argv)
    m=MainWindow()
    m.show()
    exit(a.exec_())
