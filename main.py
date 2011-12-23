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

        self.black_color = (0, 0, 0)
        self.white_color = (255, 255, 255)
        self.red_color = (255, 0, 0)
        self.yellow_color = (255, 255, 0)
        self.green_color = (0, 255, 0)
        self.light_blue_color = (0, 255, 255)
        self.blue_color = (0, 0, 255)
        self.purple_color = (255, 0, 255)

        self.starting_color = self.blue_color
        self.ending_color = self.red_color
        self.color_difference = (self.ending_color[0] - self.starting_color[0],
                                 self.ending_color[1] - self.starting_color[1],
                                 self.ending_color[2] - self.starting_color[2])
                                    
        
        # The bounds of the complex plane that is being viewed.
        # comp_y_max, or the upper imaginary-axis bound, is dynamically generated
        # based on the other 3 bounds and the aspect ratio of the window. This prevents stretching. 
        self.comp_x_min = -2
        self.comp_x_max = 1
        self.comp_y_min = -1.2
        
        # The number of iterations to run through the mandelbrot algorithm.
        self.iteration = 100

    def set_starting_color(self, color):
        if color == 'Black':
            self.starting_color = self.black_color
        elif color == 'White':
            self.starting_color = self.white_color
        elif color == 'Red':
            self.starting_color = self.red_color
        elif color == 'Yellow':
            self.starting_color = self.yellow_color
        elif color == 'Green':
            self.starting_color = self.green_color
        elif color == 'Light Blue':
            self.starting_color = self.light_blue_color
        elif color == 'Blue':
            self.starting_color = self.blue_color
        elif color == 'Purple':
            self.starting_color = self.purple_color

        self.color_difference = (self.ending_color[0] - self.starting_color[0],
                                 self.ending_color[1] - self.starting_color[1],
                                 self.ending_color[2] - self.starting_color[2])

    def generateMandelbrot(self):
        self.generate = True
        self.update()

    def set_color(self, color_percent):
        red_value = int((self.color_difference[0] * color_percent) + self.starting_color[0])
        green_value = int((self.color_difference[1] * color_percent) + self.starting_color[1])
        blue_value = int((self.color_difference[2] * color_percent) + self.starting_color[2])
        self.painter.setPen(QtGui.QColor(red_value, green_value, blue_value))
        
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
        #TODO: Paint to a QPixmap or QImage instead of directly to the widget.
        self.painter.begin(self)
        
        self.painter.setPen(self.color1)
        self.painter.setFont(self.font)
        
        if self.generate:
            # Generates the last view-window bound.
            self.comp_y_max = self.comp_y_min + float(self.comp_x_max - self.comp_x_min) * self.height() / self.width()
            
            # Part of the linear interpolation formula generated here to save processing time.
            self.real_lerp = float(self.comp_x_max - self.comp_x_min)/self.width()
            self.img_lerp = float(self.comp_y_max - self.comp_y_min)/self.height()
            print "Generating Fractal..."
            for x in range(self.width()):
                for y in range(self.height()):
                    i = self.point_is_in_set(x, y)
                    if i == self.iteration: # if the point remained bounded for every iteration
                        self.painter.setPen(self.color1) # black
                    
                    # Escape-time coloring.
                    # Color goes from black to {color} for the first slice of the iterations
                    # Color goes from {color} to white for the second slice of the iterations
                    else:
                        slice = self.iteration * 0.5
                        if i < slice:
                            color_percent = float(i) / slice
                            self.set_color(color_percent)
                        else:
                            color_percent = (i - slice)/(self.iteration - slice)
                            self.set_color(color_percent)
                    self.painter.drawPoint(x, y)
                if x % 80 == 0: #temporary loading indicator
                    loading = "{0}%".format(int(round(float(x) / self.width() * 100)))
                    print loading
            self.generate = False
            self.menu = False
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

    def set_starting_color(self):
        text = self.sender().text()
        self.grapher.set_starting_color(text)
    
    def createActions(self):
        self.genAct = QtGui.QAction("&Generate", self)
        self.genAct.triggered.connect(self.grapher.generateMandelbrot)

        self.start_black = QtGui.QAction('Black', self)
        self.start_black.triggered.connect(self.set_starting_color)
        self.start_white = QtGui.QAction('White', self)
        self.start_white.triggered.connect(self.set_starting_color)
        self.start_red = QtGui.QAction('Red', self)
        self.start_red.triggered.connect(self.set_starting_color)
        self.start_yellow = QtGui.QAction('Yellow', self)
        self.start_yellow.triggered.connect(self.set_starting_color)
        self.start_green = QtGui.QAction('Green', self)
        self.start_green.triggered.connect(self.set_starting_color)
        self.start_light_blue = QtGui.QAction('Light Blue', self)
        self.start_light_blue.triggered.connect(self.set_starting_color)
        self.start_blue = QtGui.QAction('Blue', self)
        self.start_blue.triggered.connect(self.set_starting_color)
        self.start_purple = QtGui.QAction('Purple', self)
        self.start_purple.triggered.connect(self.set_starting_color)

        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.genAct)

        self.start_color_menu = self.menuBar().addMenu('Starting Color')

        self.start_color_menu.addAction(self.start_black)
        self.start_color_menu.addAction(self.start_white)
        self.start_color_menu.addAction(self.start_red)
        self.start_color_menu.addAction(self.start_yellow)
        self.start_color_menu.addAction(self.start_green)
        self.start_color_menu.addAction(self.start_light_blue)
        self.start_color_menu.addAction(self.start_blue)
        self.start_color_menu.addAction(self.start_purple)
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
