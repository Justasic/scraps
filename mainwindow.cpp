#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "md5.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    comboselected(0)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

// Exit button
void MainWindow::on_pushButton_2_clicked()
{
    exit(0);
}

// Upper text box -> lineEdit
// Lower text box -> lineEdit_2
void MainWindow::on_lineEdit_textChanged(const QString &arg1)
{
    switch(this->comboselected)
    {
        case 0:
            if(arg1.isEmpty())
                this->ui->lineEdit_2->setText("Enter some text");
            else
                this->ui->lineEdit_2->setText(QString().fromStdString(md5(arg1.toStdString())));
            break;
        case 1:
            if(arg1.isEmpty())
                this->ui->lineEdit_2->setText("Enter some text");
            else
                this->ui->lineEdit_2->setText(arg1);
        default:
            break;
    }
}

void MainWindow::on_comboBox_currentIndexChanged(int index)
{
    this->comboselected = index;
}
