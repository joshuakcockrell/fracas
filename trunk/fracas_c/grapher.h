#ifndef GRAPHER_H
#define GRAPHER_H

#include <QWidget>
#include <QList>

class Grapher : public QWidget
{
    Q_OBJECT

public:
    Grapher(QWidget *parent = 0);
    QColor getOuterColor();
    QColor getMiddleColor();
    QColor getInnerColor();
    QColor getFractalColor();
    void setOuterColor(QColor color);
    void setMiddleColor(QColor color);
    void setInnerColor(QColor color);
    void setFractalColor(QColor color);

public slots:
    void generateFractal();

protected:
    void paintEvent(QPaintEvent *event);
    void changeEvent(QEvent *event);

private:
    QWidget *parent;
    QImage image;

    //fractal
    bool generate;
    float comp_xMin;
    float comp_xMax;
    float comp_yMin;
    float comp_yMax;
    float realLerp;
    float imgLerp;
    int iterations;
    int slice;
    int pointInSet(const int &screenX, const int &screenY);

    //colors
    QColor fractalColor;
    QColor outerColor;
    QColor middleColor;
    QColor innerColor;
    QList<int> midColorDiff;
    QList<int> innerColorDiff;

};

#endif // GRAPHER_H
