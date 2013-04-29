#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <cstdio>

extern QString SHA1Hash(QString str);
extern QString SHA256Hash(QString str);
extern QString SHA1Hash(QString str);
extern std::string md5(const std::string str);
extern bool BlakeHash(QString &rethash, const QString &text);

QString printfify(const char *fmt, ...)
{
    if(fmt)
    {
        va_list args;
        char buf[65536];
        va_start(args, fmt);
        vsnprintf(buf, sizeof(buf), fmt, args);
        va_end(args);
        return buf;
    }
    else
        return fmt;
}

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

void MainWindow::TextChanged(QString text)
{
    if(text.isEmpty())
    {
        this->ui->lineEdit_2->setText("Enter some text");
        return;
    }

    switch(this->comboselected)
    {
        case 0: // MD5
            this->ui->lineEdit_2->setText(QString().fromStdString(md5(text.toStdString())));
            break;
        case 1: // MD4
            //this->ui->lineEdit_2->setText();
            break;
        case 2: // SHA-1
            this->ui->lineEdit_2->setText(SHA1Hash(text));
            break;
        case 3: // SHA-2
            //this->ui->lineEdit_2->setText();
            break;
        case 4: // SHA-3
            //this->ui->lineEdit_2->setText();
            break;
        case 5: // SHA-256
            this->ui->lineEdit_2->setText(SHA256Hash(text));
            break;
        case 6: // SHA-384
            //this->ui->lineEdit_2->setText();
            break;
        case 7: // SHA-512
            //this->ui->lineEdit_2->setText();
            break;
        case 8: // RIPEMD-128
            //this->ui->lineEdit_2->setText();
            break;
        case 9: // RIPEMD-160
            //this->ui->lineEdit_2->setText();
            break;
        case 10: // Whirlpool
            //this->ui->lineEdit_2->setText();
            break;
        case 11: // GOST
            //this->ui->lineEdit_2->setText();
            break;
        case 11: // Tiger
            //this->ui->lineEdit_2->setText();
            break;
        case 11: // Skein
            //this->ui->lineEdit_2->setText();
            break;
        case 11: // Blake
            QString str;
            if(BlakeHash(str, text))
                this->ui->lineEdit_2->setText(str);
            break;
        case 8: // NONE
            this->ui->lineEdit_2->setText(text);
            break;
        default:
            break;
    }
}

// Upper text box -> lineEdit
// Lower text box -> lineEdit_2
void MainWindow::on_lineEdit_textChanged(const QString &arg1)
{
    this->TextChanged(arg1);
}

void MainWindow::on_comboBox_currentIndexChanged(int index)
{
    this->comboselected = index;
    this->TextChanged(this->ui->lineEdit->text());
}
