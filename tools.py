from PySide import QtGui

def add_color_diff((r, g, b), color2, multi = 1):
    red = r * multi + color2.red()
    green = g * multi + color2.green()
    blue = b * multi + color2.blue()
    return QtGui.QColor(red, green, blue)
    
def color_diff(color1, color2):
    r = color1.red() - color2.red()
    g = color1.green() - color2.green()
    b = color1.blue() - color2.blue()
    return r, g, b