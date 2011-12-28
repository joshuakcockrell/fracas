#include <QtGui>

#include "mainwindow.h"
#include "grapher.h"

MainWindow::MainWindow()
{
    resize(600, 500);
    setWindowTitle("fracas");
    grapher = new Grapher(this);
    setCentralWidget(grapher);
    createActions();
    createMenus();
}

void MainWindow::createActions()
{
    //File
    generateAct = new QAction("&Generate", this);
    connect(generateAct, SIGNAL(triggered()), grapher, SLOT(generateFractal()));

    //Colors

    iconPainter = new QPainter();
    iconSize = new QSize(64, 64);
    outerIcon = new QPixmap(*iconSize);
    middleIcon = new QPixmap(*iconSize);
    innerIcon = new QPixmap(*iconSize);
    fractalIcon = new QPixmap(*iconSize);

    setIconColor(outerIcon, grapher->getOuterColor());
    setIconColor(middleIcon, grapher->getMiddleColor());
    setIconColor(innerIcon, grapher->getInnerColor());
    setIconColor(fractalIcon, grapher->getFractalColor());

    outerColorAct = new QAction(*outerIcon, "&Outer Color", this);
    middleColorAct = new QAction(*middleIcon, "&Middle Color", this);
    innerColorAct = new QAction(*innerIcon, "&Inner Color", this);
    fractalColorAct = new QAction(*fractalIcon, "&Fractal COlor", this);

    csignalMapper = new QSignalMapper(this);
    connect(outerColorAct, SIGNAL(triggered()), csignalMapper, SLOT(map()));
    connect(middleColorAct, SIGNAL(triggered()), csignalMapper, SLOT(map()));
    connect(innerColorAct, SIGNAL(triggered()), csignalMapper, SLOT(map()));
    connect(fractalColorAct, SIGNAL(triggered()), csignalMapper, SLOT(map()));

    csignalMapper->setMapping(outerColorAct, 1);
    csignalMapper->setMapping(middleColorAct, 2);
    csignalMapper->setMapping(innerColorAct, 3);
    csignalMapper->setMapping(fractalColorAct, 4);

    connect(csignalMapper, SIGNAL(mapped(int)), this, SLOT(setColor(int)));
}

void MainWindow::createMenus()
{
    fileMenu = new QMenu("&File", this);
    fileMenu->addAction(generateAct);

    colorMenu = new QMenu("&Colors", this);
    colorMenu->addAction(outerColorAct);
    colorMenu->addAction(middleColorAct);
    colorMenu->addAction(innerColorAct);
    colorMenu->addAction(fractalColorAct);

    menuBar()->addMenu(fileMenu);
    menuBar()->addMenu(colorMenu);
}

void MainWindow::setColor(int id)
{
    QColorDialog cDialog;
    QColor color;
    switch (id)
    {
    case 1:
        color = cDialog.getColor(grapher->getOuterColor(), this, "Outer Color");
        grapher->setOuterColor(color);
        setIconColor(outerIcon, color);
        outerColorAct->setIcon(*outerIcon);
        break;
    case 2:
        color = cDialog.getColor(grapher->getMiddleColor(), this, "Middle Color");
        grapher->setMiddleColor(color);
        setIconColor(middleIcon, color);
        middleColorAct->setIcon(*middleIcon);
        break;
    case 3:
        color = cDialog.getColor(grapher->getInnerColor(), this, "Inner Color");
        grapher->setInnerColor(color);
        setIconColor(innerIcon, color);
        innerColorAct->setIcon(*innerIcon);
        break;
    case 4:
        color = cDialog.getColor(grapher->getFractalColor(), this, "Fractal Color");
        grapher->setFractalColor(color);
        setIconColor(fractalIcon, color);
        fractalColorAct->setIcon(*fractalIcon);
        break;


    }
    grapher->generateFractal();
}

void MainWindow::setIconColor(QPixmap *icon, QColor color)
{
    iconPainter->begin(icon);
    iconPainter->fillRect(icon->rect(), color);
    iconPainter->end();
}
