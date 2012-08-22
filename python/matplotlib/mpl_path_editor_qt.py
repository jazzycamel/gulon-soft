from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np

Path = mpath.Path
epsilon=5

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

        self._ind=None
        self.showVerts=True

        QVBoxLayout(self)

        self.figure=Figure()
        self.canvas=FigureCanvas(self.figure)
        self.canvas.setParent(self)

        codes, verts = zip(*pathdata)
        path = mpath.Path(verts, codes)
        self.patch = mpatches.PathPatch(path, facecolor='red', edgecolor='yellow', alpha=0.5)
        self.axes=self.figure.add_subplot(111)
        self.axes.add_patch(self.patch)
        self.patch.set_animated(True)

        x,y=zip(*path.vertices)
        self.line,=self.axes.plot(x, y, 'go-', animated=True)

        self.axes.grid()
        self.axes.set_xlim(-3,4)
        self.axes.set_ylim(-3,4)

        self.axes.set_title('spline paths')

        self.canvas.mpl_connect('draw_event', self.drawCallback)
        self.canvas.mpl_connect('button_press_event', self.buttonPressCallback)
        self.canvas.mpl_connect('button_release_event', self.buttonReleaseCallback)
        self.canvas.mpl_connect('motion_notify_event', self.motionNotifyCallback)

        self.layout().addWidget(self.canvas)

    # Callbacks
    def drawCallback(self, event):
        self.background = self.canvas.copy_from_bbox(self.axes.bbox)
        self.axes.draw_artist(self.patch)
        self.axes.draw_artist(self.line)
        self.canvas.blit(self.axes.bbox)

    def buttonPressCallback(self, event):
         if (not self.showVerts) or (event.inaxes==None) or (event.button!=1): return
         self._ind=self.getIndUnderPoint(event)

    def buttonReleaseCallback(self, event):
        if (not self.showVerts) or (event.button!=1): return
        self._ind=None

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_T:
            self.showVerts=not self.showVerts
            self.line.set_visible(self.showVerts)
            if not self.showVerts: self._ind=None
            self.canvas.draw()
            event.accept()
        else: QWidget.keyPressEvent(self, event)     

    def motionNotifyCallback(self, event):
        if (not self.showVerts) or (self._ind==None) or (event.inaxes==None) or (event.button!=1): return

        x,y=event.xdata,event.ydata
        vertices=self.patch.get_path().vertices
        vertices[self._ind]=x,y
        self.line.set_data(zip(*vertices))

        self.canvas.restore_region(self.background)
        self.axes.draw_artist(self.patch)
        self.axes.draw_artist(self.line)
        self.canvas.blit(self.axes.bbox)

    # Other methods
    def getIndUnderPoint(self, event):
        xy=np.asarray(self.patch.get_path().vertices)
        xyt=self.patch.get_transform().transform(xy)
        xt,yt=xyt[:,0],xyt[:,1]
        d=np.sqrt((xt-event.x)**2 + (yt-event.y)**2)
        ind=d.argmin()

        if d[ind]>=epsilon: ind=None
        return ind

if __name__=="__main__":
    from sys import argv, exit
    a=QApplication(argv)
    w=Widget()
    w.show()
    exit(a.exec_())
