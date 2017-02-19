#include "widget.h"
#include "ui_widget.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
    connect(ui->pushButton,SIGNAL(clicked(bool)),this,SLOT(readjson()));
    connect(ui->pushButton_2,SIGNAL(clicked(bool)),this,SLOT(testpy()));
    data=0;
    num=0;
}

Widget::~Widget()
{
    delete ui;
    delete[] data;
}

myData* Widget::readjson()
{
    QString val;
    QFile file("D:/Qt/mypro/pasejson3/data.json");
    if (!file.open(QIODevice::ReadOnly)) {
            qDebug() << "Open file failed.";
            return 0;
    }
    val = file.readAll();
    file.close();

    QJsonDocument d = QJsonDocument::fromJson(val.toUtf8());
    if(d.isArray())
    {
         qDebug() <<"array";
    }
    QJsonArray array = d.array();
    int size = array.size();
    qDebug() <<size;
    data=new myData[size];
    for(int i=0;i<size;i++)
    {
        QJsonObject sett2=array.at(i).toObject();
        //QJsonObject sett2 = d.object();

        QJsonValue value = sett2.value(QString("faceAttributes"));
        QJsonObject item = value.toObject();
        data[i].age=item["age"].toDouble();
        qDebug()<<data[i].age;

        if(item["gender"].toString()=="female")//女为假
        {
            data[i].gender=false;
            qDebug()<<data[i].gender;
        }

        data[i].smile=item["smile"].toDouble();
        qDebug()<<data[i].smile;

        if(item["glasses"].toString()!="NoGlasses")//不带眼镜为假
        {
            data[i].glasses=true;
            qDebug()<<item["glasses"].toString();
        }

        QJsonObject item2=item["facialHair"].toObject();
        data[i].facialHair[0]=item2["moustache"].toDouble();
        data[i].facialHair[1]=item2["beard"].toDouble();
        data[i].facialHair[2]=item2["sideburns"].toDouble();

        qDebug()<<data[i].facialHair[0]<<data[i].facialHair[1]<<data[i].facialHair[2];
    }
    num=size;

    return data;
}
void Widget::testpy()
{
    QProcess p(0);
    //p.start("python", QStringList()<<"/c"<<"test.py");
    p.start("cmd", QStringList()<<"/c"<<"python d:/Qt/mypro/pasejson3/test.py https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1481365593&di=35ddf903d99e592eaf9188e03dfbd824&src=http://img1.juimg.com/140914/330660-1409141Q15795.jpg");
     p.waitForStarted();
     p.waitForFinished();
     qDebug()<<"good";
}
