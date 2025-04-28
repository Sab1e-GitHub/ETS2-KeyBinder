#ifndef ETS2KEYBINDERWIZARD_H
#define ETS2KEYBINDERWIZARD_H

#include "BigKey.hpp"
#include "global.h"
#include <QDir>
#include <QWizard>
#include <dinput.h>
#include <string.h>
#include <windows.h>


namespace Ui {
class ETS2KeyBinderWizard;
}

class ETS2KeyBinderWizard : public QWizard {
    Q_OBJECT

public:
    explicit ETS2KeyBinderWizard(QWidget* parent = nullptr);
    ~ETS2KeyBinderWizard();

    QStringList getDeviceNameGameList();

private slots:

    void on_comboBox_activated(int index);

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void on_comboBox_3_activated(int index);

    void on_comboBox_2_activated(int index);

    void on_checkBox_2_clicked(bool checked);

    void on_checkBox_3_clicked(bool checked);

    void on_checkBox_4_clicked(bool checked);

private:
    Ui::ETS2KeyBinderWizard* ui;

    std::string deviceName;     // 硬件设备名称
    std::string gameDeviceName; // 游戏输入设备名称

    QStringList gameJoyPosNameList = {
        "joy ", "joy2", "joy3", "joy4", "joy5",
    };
    QString steamProfiles[2] = {QDir::homePath() + "/Documents/Euro Truck Simulator 2/steam_profiles",
                                QDir::homePath() + "/Documents/American Truck Simulator/steam_profiles"};
    QString profiles[2] = {QDir::homePath() + "/Documents/Euro Truck Simulator 2/profiles",
                           QDir::homePath() + "/Documents/American Truck Simulator/profiles"};
    QString selectedProfilePath; // 选择的配置文件路径

    QList<QPair<QString, QDateTime>> steamProfileFolders;
    QList<QPair<QString, QDateTime>> profileFolders; // 所有配置文件列表

    LPDIRECTINPUT8 pDirectInput = NULL;
    LPDIRECTINPUTDEVICE8 pDevice = NULL;
    int lastDeviceIndex = -99;
    DIDEVCAPS capabilities;

    BigKey getKeyState();

    bool hasLastDevInCurrentDeviceList(std::string lastDeviceName);
    bool openDiDevice(int deviceIndex, HWND hWnd);
    void scanDevice();
    bool initDirectInput();

    void updateUserProfile();
    bool backupProfile();

    bool generateMappingFile(int keyIndex1, int keyIndex2, bool multiBtnFlag);
};

#endif // ETS2KEYBINDERWIZARD_H
