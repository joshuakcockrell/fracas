import sys

from PySide import QtCore, QtGui
from tools import add_color_diff, color_diff

class Grapher(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Grapher, self).__init__()
        
        self.generate = False
        self.fractal_color = QtGui.QColor(0, 0, 0)
        self.outer_color = QtGui.QColor(0, 0, 0)
        self.middle_color = QtGui.QColor(255, 0, 0)
        self.inner_color = QtGui.QColor(255, 255, 255)
        self.mid_color_diff = color_diff(self.middle_color, self.outer_color)
        self.inner_color_diff = color_diff(self.inner_color, self.middle_color)
        
        # The bounds of the complex plane that is being viewed.
        # comp_y_max, or the upper imaginary-axis bound, is dynamically generated
        # based on the other 3 bounds and the aspect ratio of the window. This prevents stretching. 
        self.comp_x_min = -2
        self.comp_x_max = 1
        self.comp_y_min = -1.2
        
        # The number of iterations to run through the mandelbrot algorithm.
        self.iteration = 70
    
    def setOuterColor(self, color):
        self.outer_color = color
        self.mid_color_diff = color_diff(self.middle_color, self.outer_color)
    
    def setMiddleColor(self, color):
        self.middle_color = color
        self.mid_color_diff = color_diff(self.middle_color, self.outer_color)
        self.inner_color_diff = color_diff(self.inner_color, self.middle_color)
    
    def setInnerColor(self, color):
        self.inner_color = color
        self.inner_color_diff = color_diff(self.inner_color, self.middle_color)
        
    def setFractalColor(self, color):
        self.fractal_color = color
        
    def generateMandelbrot(self):
        window.setFixedSize(window.size())
        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        painter = QtGui.QPainter(self.image)
        self.comp_y_max = self.comp_y_min + float(self.comp_x_max - self.comp_x_min) * self.height() / self.width()
        # Part of the linear interpolation formula generated here to save processing time.
        self.real_lerp = float(self.comp_x_max - self.comp_x_min)/self.width()
        self.img_lerp = float(self.comp_y_max - self.comp_y_min)/self.height()
        loading_percent = self.width() / 100
        window.statusBar().addWidget(window.progressBar, 1)
        window.progressBar.show()
        print "Generating Fractal..."
        for x in range(self.width()):
            for y in range(self.height()):
                i = self.point_is_in_set(x, y)
                if i == self.iteration: # if the point remained bounded for every iteration
                    painter.setPen(self.fractal_color)
                
                # Escape-time coloring.
                # Color goes from black to {color} for the first slice of the iterations
                # Color goes from {color} to white for the second slice of the iterations
                else:
                    slice = self.iteration * 0.5
                    if i < slice:
                        percent = float(i) / slice
                        rgb = add_color_diff(self.mid_color_diff, self.outer_color, percent)
                        painter.setPen(QtGui.QColor(rgb))
                    else:
                        percent = (i - slice)/(self.iteration - slice)
                        rgb = add_color_diff(self.inner_color_diff, self.middle_color, percent)
                        painter.setPen(QtGui.QColor(rgb))
                painter.drawPoint(x, y)
            if x % loading_percent == 0: #temporary loading indicator
                # loading = "{0}%".format(x / loading_percent)
                loading = x / loading_percent
                window.progressBar.setValue(loading)
        self.generate = True
        print "Done!"
        window.statusBar().removeWidget(window.progressBar)
        window.statusBar().showMessage("Done!")
        self.update()
    
    # Mandelbrot algorithm that checks whether a certain point is in the set
    def point_is_in_set(self, x, y):
        # Linear interpolation that interpolates the window's pixel coordinate point
        # to the respective point on the complex plane.
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
            i += 1
        
        return i
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.generate:
            painter.drawImage(QtCore.QPoint(0, 0), self.image)
        
        else:
            painter.setPen(QtCore.Qt.white)
            painter.setFont(QtGui.QFont("Arial", window.width()/25, 100))
            painter.fillRect(self.rect(), QtCore.Qt.black)
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Ready to generate Mandelbrot")    

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(800, 700)
        self.setWindowTitle("fracas")
        self.grapher = Grapher(self)
        self.setCentralWidget(self.grapher)
        self.createActions()
        self.createMenus()
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setFormat("")
        self.statusBar().showMessage("Ready")
      
    def setColor(self):
        sender = self.sender()
        if sender.data() == "outer":
            color = QtGui.QColorDialog.getColor(self.grapher.outer_color, self)
            if color.isValid():
                self.grapher.setOuterColor(color)
                self.icon_color(self.outer_pix, color)
                self.outerColorAct.setIcon(self.outer_pix)
        
        elif sender.data() == "middle":
            color = QtGui.QColorDialog.getColor(self.grapher.middle_color, self)
            if color.isValid():
                self.grapher.setMiddleColor(color)
                self.icon_color(self.middle_pix, color)
                self.middleColorAct.setIcon(self.middle_pix)
        
        elif sender.data() == "inner":
            color = QtGui.QColorDialog.getColor(self.grapher.inner_color, self)
            if color.isValid():
                self.grapher.setInnerColor(color)
                self.icon_color(self.inner_pix, color)
                self.innerColorAct.setIcon(self.inner_pix)
        
        elif sender.data() == "fractal":
            color = QtGui.QColorDialog.getColor(self.grapher.fractal_color, self)
            if color.isValid():
                self.grapher.setFractalColor(color)
                self.icon_color(self.fractal_pix, color)
                self.fractalColorAct.setIcon(self.fractal_pix)
    
        
    def createActions(self):
        self.genAct = QtGui.QAction("&Generate", self)
        self.genAct.triggered.connect(self.grapher.generateMandelbrot)
        
        self.i_painter = QtGui.QPainter()
        self.outer_pix = QtGui.QPixmap(self.size())
        self.middle_pix = QtGui.QPixmap(self.size())
        self.inner_pix = QtGui.QPixmap(self.size())
        self.fractal_pix = QtGui.QPixmap(self.size())
        
        self.icon_color(self.outer_pix, self.grapher.outer_color)
        self.icon_color(self.middle_pix, self.grapher.middle_color)
        self.icon_color(self.inner_pix, self.grapher.inner_color)
        self.icon_color(self.fractal_pix, self.grapher.fractal_color)
        
        self.outerColorAct = QtGui.QAction(self.outer_pix, 'Outer Color', self, triggered=self.setColor)
        self.outerColorAct.setData("outer")
        self.middleColorAct = QtGui.QAction(self.middle_pix, 'Middle Color', self, triggered=self.setColor)
        self.middleColorAct.setData("middle")
        self.innerColorAct = QtGui.QAction(self.inner_pix, 'Inner Color', self, triggered=self.setColor)
        self.innerColorAct.setData("inner")
        self.fractalColorAct = QtGui.QAction(self.fractal_pix, 'Fractal Color', self, triggered=self.setColor)
        self.fractalColorAct.setData("fractal")

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.genAct)

        self.start_color_menu = self.menuBar().addMenu('Colors')

        self.start_color_menu.addAction(self.outerColorAct)
        self.start_color_menu.addAction(self.middleColorAct)
        self.start_color_menu.addAction(self.innerColorAct)
        self.start_color_menu.addAction(self.fractalColorAct)
    
    def icon_color(self, pix, color):
        self.i_painter.begin(pix)
        self.i_painter.fillRect(self.rect(), color)
        self.i_painter.end() 

             
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
