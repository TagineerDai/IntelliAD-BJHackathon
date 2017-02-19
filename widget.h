#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include<QFile>
#include<QDebug>
#include<QProcess>

#include<QIODevice>
#include<QJsonDocument>
#include<QJsonObject>
#include<QJsonValue>
#include<QJsonArray>

struct myData
{
  int age;
  bool gender;
  float smile;
  float facialHair[3];
  bool glasses;
};
namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    myData* data;
    int num;
    ~Widget();
    int count(){return num;}
public slots:
    myData* readjson();
    void testpy();

private:
    Ui::Widget *ui;
};

#endif // WIDGET_H
