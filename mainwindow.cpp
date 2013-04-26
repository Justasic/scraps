#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "md5.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
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

// Okay button
void MainWindow::on_pushButton_clicked()
{
    QString arg1 = this->ui->lineEdit->text();
    if(arg1.isEmpty())
        this->ui->lineEdit_2->setText("Enter some text, nigger.");
    else
        this->ui->lineEdit_2->setText(QString().fromStdString(md5(arg1.toStdString())));
}

// Upper text box -> lineEdit
// Lower text box -> lineEdit_2
void MainWindow::on_lineEdit_textChanged(const QString &arg1)
{
    if(arg1.isEmpty())
        this->ui->lineEdit_2->setText("Enter some text, nigger.");
    else
        this->ui->lineEdit_2->setText(QString().fromStdString(md5(arg1.toStdString())));
}
