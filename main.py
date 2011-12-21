import sys
from PySide import QtCore, QtGui

class Grapher(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Grapher, self).__init__()
        print "Center Widget Launched"
        
        self.generate = False
        self.colorb = QtCore.Qt.black
        self.color1 = QtCore.Qt.white
        self.color2 = QtCore.Qt.darkGray
        self.font = QtGui.QFont("Arial", 30, 100)
        self.qp = QtGui.QPainter()
        
    def generateMandelbrot(self):
        self.generate = True
        self.update()
        print "Generating Fractal"
    
    def paintEvent(self, event):
        self.qp.begin(self)
        
        self.qp.setPen(self.color1)
        self.qp.setBrush(self.color2)
        self.qp.setFont(self.font)
        
        self.qp.fillRect(self.rect(), self.colorb)
        
        if not self.generate:
            self.qp.drawText(self.rect(), QtCore.Qt.AlignCenter, "Ready to generate Mandelbrot")
        
        if self.generate:
            self.qp.drawText(self.rect(), QtCore.Qt.AlignCenter, "Waalaa")
        
        self.qp.end()
        
    def mousePressEvent(self, event):
        self.generateMandelbrot()

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("fracas")
        self.grapher = Grapher(self)
        self.setCentralWidget(self.grapher)
        self.createActions()
        self.createMenus()
    
    def createActions(self):
        self.genAct = QtGui.QAction("&Generate", self)
        self.genAct.triggered.connect(self.grapher.generateMandelbrot)
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.genAct)
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())