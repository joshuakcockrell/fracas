#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QSignalMapper>
//#include <QPixMap>

class Grapher;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
   MainWindow();

public slots:
   void setColor(int id);

private:
    Grapher *grapher;

    //Actions
    void createActions();
    void setIconColor(QPixmap *icon, QColor color);

    QPainter *iconPainter;
    QSize *iconSize;
    QPixmap *outerIcon;
    QPixmap *middleIcon;
    QPixmap *innerIcon;
    QPixmap *fractalIcon;

    QAction *generateAct;
    QAction *outerColorAct;
    QAction *middleColorAct;
    QAction *innerColorAct;
    QAction *fractalColorAct;
    QSignalMapper *csignalMapper;

    //Menus
    void createMenus();
    QMenu *fileMenu;
    QMenu *colorMenu;
};
#endif // MAINWINDOW_H
