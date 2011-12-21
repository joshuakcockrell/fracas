import sys
from PySide import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        print self.width
        self.screen_width = 600
        self.screen_height = 400

        self.initQuitButton()
        self.initUI()

    def quit_program(self):
        return QtCore.QCoreApplication.instance().quit

    def initQuitButton(self):
        quit_button = QtGui.QPushButton('Quit button', self)
        
        quit_button.clicked.connect(self.quit_program()) # quitting
        
        quit_shape = quit_button.sizeHint()
        quit_size = [quit_shape.width(), quit_shape.height()]
        quit_button.resize(quit_shape)
        top = 0
        left = self.screen_width - quit_size[0]
        quit_button.move(left, top) # topleft

    def initUI(self):               
        self.setGeometry(10, 30, self.screen_width, self.screen_height) # size of window
        self.setWindowTitle('Quit button')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
