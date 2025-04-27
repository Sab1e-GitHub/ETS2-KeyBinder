QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    ets2keybinderwizard.cpp \
    global.cpp \
    main.cpp \


HEADERS += \
    device_info.h \
    ets2keybinderwizard.h \
    global.h \

FORMS += \
    ets2keybinderwizard.ui \

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target



#win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../release/ -lhidapi
#else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../debug/ -lhidapi

INCLUDEPATH += $$PWD/SCS_Telemetry
# DEPENDPATH += $$PWD/.

#LIBS += -L$$PWD/ -lhidapi

# LIBS += -L$$PWD/ -lViGEmClient

LIBS += -ldinput8 -ldxguid

RESOURCES += \
    resource.qrc

RC_FILE = appicon.rc
