#-------------------------------------------------
#
# Project created by QtCreator 2013-04-25T21:28:56
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = keygen
TEMPLATE = app

SOURCES += main.cpp\
        mainwindow.cpp \
        md5.cpp \
        sha1.cpp \
        sha256.cpp \
    blake.cpp

HEADERS  += mainwindow.h \
    md5.h \
    sha1.h

FORMS    += mainwindow.ui
