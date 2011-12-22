import sys
from PySide import QtCore, QtGui

class Grapher(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Grapher, self).__init__()
        
        self.generate = False
        self.menu = True
        self.colorb = QtCore.Qt.white
        self.color1 = QtCore.Qt.black
        self.fractColor = QtCore.Qt.darkGray
        self.font = QtGui.QFont("Arial", 30, 100)
        self.painter = QtGui.QPainter()
        
        self.comp_x_min = -2
        self.comp_x_max = 1
        self.comp_y_min = -1.2
        
        self.iteration = 100
        
         
    def generateMandelbrot(self):
        self.generate = True
        self.update()

    def point_is_in_set(self, x, y):
        comp_x = self.comp_x_min + x * self.real_lerp
        comp_y = self.comp_y_max - y * self.img_lerp
        iter_x = comp_x
        iter_y = comp_y

        for i in range(0, self.iteration):
            iter_x2 = iter_x**2
            iter_y2 = iter_y**2
            if (iter_x2 + iter_y2 > 4):
                return i
            iter_y = 2 * iter_x * iter_y + comp_y    
            iter_x = iter_x2 - iter_y2 + comp_x
            i = i + 1
        
        return i
    
    def paintEvent(self, event):
        self.painter.begin(self)
        
        self.painter.setPen(self.color1)
        self.painter.setFont(self.font)
        
        if self.generate:
            self.comp_y_max = self.comp_y_min + float(self.comp_x_max - self.comp_x_min) * self.height() / self.width()
            self.real_lerp = float(self.comp_x_max - self.comp_x_min)/self.width()
            self.img_lerp = float(self.comp_y_max - self.comp_y_min)/self.height()
            print "Generating Fractal..."
            for x in range(self.width()):
                for y in range(self.height()):
                    i = self.point_is_in_set(x, y)
                    if i == self.iteration:
                        self.painter.setPen(self.color1)
                    else:
                        slice = self.iteration * 0.5
                        if i < slice:
                            color = 255 * i / slice
                            self.painter.setPen(QtGui.QColor(color, 0, 0))
                        else:
                            color = 255 * (i - slice)/(self.iteration - slice)
                            self.painter.setPen(QtGui.QColor(255, color, color))
                    self.painter.drawPoint(x, y)
                if x % 80 == 0:
                    loading = "{0}%".format(int(round(float(x) / float(self.width()) * 100)))
                    print loading
            self.generate = False
            self.menu = False
            self.save = True
            print "Done!"
        
        elif self.menu:
            self.painter.fillRect(self.rect(), self.colorb)
            self.painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Ready to generate Mandelbrot")    
        
        self.painter.end()

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setFixedSize(1250, 1000)
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
