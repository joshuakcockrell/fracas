#include <QtCore>
#include <QtGui>
#include "grapher.h"
#include "tools.h"

Grapher::Grapher(QWidget *parent) : QWidget(parent)
{
    this->parent = parentWidget();


    //fractal
    generate = false;
    comp_xMin = -2;
    comp_xMax = 1;
    comp_yMin = -1.2;
    iterations = 200;

    //colors
    outerColor = QColor(0, 0, 0);
    middleColor = QColor(255, 0, 0);
    innerColor = QColor(255, 255, 255);
    fractalColor = QColor(0, 0, 0);

    midColorDiff = colorDiff(middleColor, outerColor);
    innerColorDiff = colorDiff(innerColor, middleColor);

}

QColor Grapher::getOuterColor()
{
    return outerColor;
}

QColor Grapher::getMiddleColor()
{
    return middleColor;
}

QColor Grapher::getInnerColor()
{
    return innerColor;
}

QColor Grapher::getFractalColor()
{
    return fractalColor;
}

void Grapher::setOuterColor(QColor color)
{
    outerColor = color;
    midColorDiff = colorDiff(middleColor, outerColor);
}

void Grapher::setMiddleColor(QColor color)
{
    middleColor = color;
    midColorDiff = colorDiff(middleColor, outerColor);
    innerColorDiff = colorDiff(innerColor, middleColor);
}

void Grapher::setInnerColor(QColor color)
{
    innerColor = color;
    innerColorDiff = colorDiff(innerColor, middleColor);
}

void Grapher::setFractalColor(QColor color)
{
    fractalColor = color;
}

void Grapher::generateFractal()
{
    qDebug() << "Generating Fractal";
    //parent->setFixedSize(parent->size());
    image = QImage(size(), QImage::Format_RGB32);
    QPainter painter(&image);
    painter.fillRect(image.rect(), Qt::white);

    comp_yMax = comp_yMin + (comp_xMax - comp_xMin) * height() / width();
    realLerp = (comp_xMax - comp_xMin) / width();
    imgLerp = (comp_yMax - comp_yMin) / height();

    slice = iterations * 0.4;
    float percent;
    QColor rgb;

    for (int x=0; x<width(); x++)
    {
        for (int y = 0; y<height(); y++)
        {
            int i = pointInSet(x, y);
            if (i == iterations)
            {
                painter.setPen(fractalColor);
                //painter.drawPoint(x, y);
            }
            else
            {
                if (i < slice)
                {
                    percent = float(i) / slice;
                    rgb = addColorDiff(midColorDiff, outerColor, percent);
                }
                else
                {
                    percent = float(i - slice)/(iterations - slice);
                    rgb = addColorDiff(innerColorDiff, middleColor, percent);
                }
                painter.setPen(rgb);
            }
            painter.drawPoint(x, y);
        }
    }

    generate = true;
    update();
}

int Grapher::pointInSet(const int &screenX,const int &screenY)
{
    float x0 = comp_xMin + screenX * realLerp;
    float y0 = comp_yMax - screenY * imgLerp;
    float x = 0;
    float y = 0;
    float xTemp;
    int i = 0;
    while (x*x + y*y < 4 && i<iterations)
    {
        ++i;
        xTemp = x*x - y*y + x0;
        y = 2*x*y + y0;

        x = xTemp;
    }
    return i;
}

void Grapher::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    if (generate)
    {
        painter.fillRect(this->rect(), Qt::black);
        painter.drawImage(QPoint(0,0), image);
    }
    else
    {
        painter.setPen(Qt::white);
        painter.setFont(QFont("Arial", parent->width()/25, 100));
        painter.fillRect(this->rect(), Qt::black);
        painter.drawText(this->rect(), Qt::AlignCenter, "Ready to generate Mandelbrot");
    }

}

void Grapher::changeEvent(QEvent *event)
{
   generateFractal();
}
