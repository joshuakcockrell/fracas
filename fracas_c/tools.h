#ifndef TOOLS_H
#define TOOLS_H
QList<int> colorDiff(const QColor &color1, const QColor &color2)
{
    int r = color1.red() - color2.red();
    int g = color1.green() - color2.green();
    int b = color1.blue() - color2.blue();
    QList<int> diff;
    diff << r << g << b;
    return diff;
}

QColor addColorDiff(const QList<int> diff, const QColor &color, const float &multi = 1)
{
    int r = diff[0] * multi + color.red();
    int g = diff[1] * multi + color.green();
    int b = diff[2] * multi + color.blue();
    return QColor(r, g, b);
}

#endif // TOOLS_H
