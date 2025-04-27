#include "ets2keybinderwizard.h"
#include <QApplication>

int main(int argc, char* argv[]) {
    QApplication a(argc, argv);
    ETS2KeyBinderWizard w;

    w.show();
    return a.exec();
}
