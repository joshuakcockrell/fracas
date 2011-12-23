import sys

from PySide import QtCore, QtGui

class Grapher(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Grapher, self).__init__()
        
        self.generate = False

        self.black_color = (0, 0, 0)
        self.white_color = (255, 255, 255)
        self.red_color = (255, 0, 0)
        self.yellow_color = (255, 255, 0)
        self.green_color = (0, 255, 0)
        self.light_blue_color = (0, 255, 255)
        self.blue_color = (0, 0, 255)
        self.purple_color = (255, 0, 255)

        self.starting_color = self.black_color
        self.mid_color = self.red_color
        self.ending_color = self.white_color
        self.mid_color_difference = (self.mid_color[0] - self.starting_color[0],
                                     self.mid_color[1] - self.starting_color[1],
                                     self.mid_color[2] - self.starting_color[2])
        
        self.end_color_difference = (self.ending_color[0] - self.mid_color[0],
                                     self.ending_color[1] - self.mid_color[1],
                                     self.ending_color[2] - self.mid_color[2])

                                    
        
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
        elif color == 'Blue':
            self.starting_color = self.blue_color

        self.mid_color_difference = (self.mid_color[0] - self.starting_color[0],
                                     self.mid_color[1] - self.starting_color[1],
                                     self.mid_color[2] - self.starting_color[2])

    def set_mid_color(self, color):
        if color == 'Black':
            self.mid_color = self.black_color
        elif color == 'White':
            self.mid_color = self.white_color
        elif color == 'Red':
            self.mid_color = self.red_color
        elif color == 'Blue':
            self.mid_color = self.blue_color

        self.mid_color_difference = (self.mid_color[0] - self.starting_color[0],
                                     self.mid_color[1] - self.starting_color[1],
                                     self.mid_color[2] - self.starting_color[2])

        self.end_color_difference = (self.ending_color[0] - self.mid_color[0],
                                     self.ending_color[1] - self.mid_color[1],
                                     self.ending_color[2] - self.mid_color[2])
    def set_ending_color(self, color):
        if color == 'Black':
            self.ending_color = self.black_color
        elif color == 'White':
            self.ending_color = self.white_color
        elif color == 'Red':
            self.ending_color = self.red_color
        elif color == 'Blue':
            self.ending_color = self.blue_color

        self.end_color_difference = (self.ending_color[0] - self.mid_color[0],
                                     self.ending_color[1] - self.mid_color[1],
                                     self.ending_color[2] - self.mid_color[2])
                                     
    def set_color(self, color_percent, destination_color, painter):

        if destination_color == 'mid':
            red_value = int((self.mid_color_difference[0] * color_percent) + self.starting_color[0])
            green_value = int((self.mid_color_difference[1] * color_percent) + self.starting_color[1])
            blue_value = int((self.mid_color_difference[2] * color_percent) + self.starting_color[2])
            painter.setPen(QtGui.QColor(red_value, green_value, blue_value))

        elif destination_color == 'end':
            red_value = int((self.end_color_difference[0] * color_percent) + self.mid_color[0])
            green_value = int((self.end_color_difference[1] * color_percent) + self.mid_color[1])
            blue_value = int((self.end_color_difference[2] * color_percent) + self.mid_color[2])
            painter.setPen(QtGui.QColor(red_value, green_value, blue_value))

    def generateMandelbrot(self):
        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        painter = QtGui.QPainter(self.image)
        self.comp_y_max = self.comp_y_min + float(self.comp_x_max - self.comp_x_min) * self.height() / self.width()
        # Part of the linear interpolation formula generated here to save processing time.
        self.real_lerp = float(self.comp_x_max - self.comp_x_min)/self.width()
        self.img_lerp = float(self.comp_y_max - self.comp_y_min)/self.height()
        print "Generating Fractal..."
        for x in range(self.width()):
            for y in range(self.height()):
                i = self.point_is_in_set(x, y)
                if i == self.iteration: # if the point remained bounded for every iteration
                    painter.setPen(QtCore.Qt.black)
                
                # Escape-time coloring.
                # Color goes from black to {color} for the first slice of the iterations
                # Color goes from {color} to white for the second slice of the iterations
                else:
                    slice = self.iteration * 0.5
                    if i < slice:
                        color_percent = float(i) / slice
                        destination_color = 'mid'
                        self.set_color(color_percent, destination_color, painter)
                    else:
                        color_percent = (i - slice)/(self.iteration - slice)
                        destination_color = 'end'
                        self.set_color(color_percent, destination_color, painter)
                painter.drawPoint(x, y)
            if x % 100 == 0: #temporary loading indicator
                loading = "{0}%".format(int(round(float(x) / self.width() * 100)))
                print loading
        self.generate = True
        print "Done!"
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
            painter.setFont(QtGui.QFont("Arial", 30, 100))
            painter.fillRect(self.rect(), QtCore.Qt.black)
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, "Ready to generate Mandelbrot")    

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

    def set_mid_color(self):
        text = self.sender().text()
        self.grapher.set_mid_color(text)

    def set_ending_color(self):
        text = self.sender().text()
        self.grapher.set_ending_color(text)
    
    def createActions(self):
        self.genAct = QtGui.QAction("&Generate", self)
        self.genAct.triggered.connect(self.grapher.generateMandelbrot)

        self.start_black = QtGui.QAction('Black', self)
        self.start_black.triggered.connect(self.set_starting_color)
        self.start_white = QtGui.QAction('White', self)
        self.start_white.triggered.connect(self.set_starting_color)
        self.start_red = QtGui.QAction('Red', self)
        self.start_red.triggered.connect(self.set_starting_color)
        self.start_blue = QtGui.QAction('Blue', self)
        self.start_blue.triggered.connect(self.set_starting_color)

        self.mid_black = QtGui.QAction('Black', self)
        self.mid_black.triggered.connect(self.set_mid_color)
        self.mid_white = QtGui.QAction('White', self)
        self.mid_white.triggered.connect(self.set_mid_color)
        self.mid_red = QtGui.QAction('Red', self)
        self.mid_red.triggered.connect(self.set_mid_color)
        self.mid_blue = QtGui.QAction('Blue', self)
        self.mid_blue.triggered.connect(self.set_mid_color)

        self.end_black = QtGui.QAction('Black', self)
        self.end_black.triggered.connect(self.set_ending_color)
        self.end_white = QtGui.QAction('White', self)
        self.end_white.triggered.connect(self.set_ending_color)
        self.end_red = QtGui.QAction('Red', self)
        self.end_red.triggered.connect(self.set_ending_color)
        self.end_blue = QtGui.QAction('Blue', self)
        self.end_blue.triggered.connect(self.set_ending_color)

        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.genAct)

        self.start_color_menu = self.menuBar().addMenu('Starting Color')

        self.start_color_menu.addAction(self.start_black)
        self.start_color_menu.addAction(self.start_white)
        self.start_color_menu.addAction(self.start_red)
        self.start_color_menu.addAction(self.start_blue)

        self.mid_color_menu = self.menuBar().addMenu('Middle Color')
        self.mid_color_menu.addAction(self.mid_black)
        self.mid_color_menu.addAction(self.mid_white)
        self.mid_color_menu.addAction(self.mid_red)
        self.mid_color_menu.addAction(self.mid_blue)

        self.end_color_menu = self.menuBar().addMenu('Ending Color')

        self.end_color_menu.addAction(self.end_black)
        self.end_color_menu.addAction(self.end_white)
        self.end_color_menu.addAction(self.end_red)
        self.end_color_menu.addAction(self.end_blue)

        
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
