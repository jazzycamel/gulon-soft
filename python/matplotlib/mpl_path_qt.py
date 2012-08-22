from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.path as mpath
import matplotlib.patches as mpatches

Path = mpath.Path

pathdata = [
    (Path.MOVETO, (1.58, -2.57)),
    (Path.CURVE4, (0.35, -1.1)),
    (Path.CURVE4, (-1.75, 2.0)),
    (Path.CURVE4, (0.375, 2.0)),
    (Path.LINETO, (0.85, 1.15)),
    (Path.CURVE4, (2.2, 3.2)),
    (Path.CURVE4, (3, 0.05)),
    (Path.CURVE4, (2.0, -0.5)),
    (Path.CLOSEPOLY, (1.58, -2.57)),
    ]

class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        QVBoxLayout(self)

        self.figure=Figure()
        self.canvas=FigureCanvas(self.figure)
        self.canvas.setParent(self)

        codes, verts = zip(*pathdata)
        path = mpath.Path(verts, codes)
        patch = mpatches.PathPatch(path, facecolor='red', edgecolor='yellow', alpha=0.5)
        self.axes=self.figure.add_subplot(111)
        self.axes.add_patch(patch)

        x,y=zip(*path.vertices)
        self.axes.plot(x, y, 'go-')

        self.axes.grid()
        self.axes.set_xlim(-3,4)
        self.axes.set_ylim(-3,4)

        self.axes.set_title('spline paths')

        self.layout().addWidget(self.canvas)

        self.canvas.draw()

if __name__=="__main__":
    from sys import argv, exit
    a=QApplication(argv)
    w=Widget()
    w.show()
    exit(a.exec_())
