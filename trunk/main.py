import sys
from PySide import QtCore, QtGui

class Grapher(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Grapher, self).__init__() #hey dude
        print "Center Widget Launched"
		
        self.generate = False
        self.colorb = QtCore.Qt.black
        self.color1 = QtCore.Qt.white
        self.color2 = QtCore.Qt.darkGray
        self.font = QtGui.QFont("Arial", 30, 100)
        self.painter = QtGui.QPainter() # painter!
        
    def generateMandelbrot(self):
	
        self.generate = True
        self.update()
        print "Generating Fractal"
    
    def paintEvent(self, event):
        self.painter.begin(self)
        
        self.painter.setPen(self.color1)
        self.painter.setBrush(self.color2)
        self.painter.setFont(self.font)
        
        self.painter.fillRect(self.rect(), self.colorb)
        
        if not self.generate:
            self.painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Ready to generate Mandelbrot")
        
        if self.generate:
            self.painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Waalaa")
        
        self.painter.end()
        
    def mousePressEvent(self, event):
        self.generateMandelbrot()

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(800, 600) # size
        self.setWindowTitle("fracas") # title
        self.grapher = Grapher(self) # making our grapher
        self.setCentralWidget(self.grapher) # SOMETHING
        self.createActions()
        self.createMenus()
    
    def createActions(self):
        self.genAct = QtGui.QAction("&Generate", self) # creating an action
        self.genAct.triggered.connect(self.grapher.generateMandelbrot) # say what the action does
		
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File") # make the file menu
        self.fileMenu.addAction(self.genAct) # add our generate action to the file menu
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())