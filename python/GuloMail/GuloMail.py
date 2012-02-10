from GmGui import GmApp
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from sys import argv
from time import sleep

if __name__=="__main__":
    app=QApplication(argv)
    splash=QSplashScreen(QPixmap("g-square.png"))
    splash.show()
    GuloMail=GmApp()
    #sleep(3)
    splash.finish(GuloMail)
    GuloMail.show()
    app.exec_()
