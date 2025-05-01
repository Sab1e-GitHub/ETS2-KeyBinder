#ifndef ETS2KEYBINDERWIZARD_H
#define ETS2KEYBINDERWIZARD_H

#include "BigKey.hpp"
#include "global.h"
#include "showkeystate.h"
#include <QDir>
#include <QWizard>
#include <dinput.h>
#include <string.h>
#include <windows.h>

// 枚举类型定义
enum class BindingType
{
    lightoff,  // 关闭灯光
    lightpark, // 示廓灯
    lighton,   // 近光灯
    lblinkerh, // 左转向灯
    rblinkerh, // 右转向灯
    hblight,   // 远光灯
    lighthorn, // 灯光喇叭
    wipers0,   // 雨刷器关闭
    wipers1,   // 雨刷器1档
    wipers2,   // 雨刷器2档
    wipers3,   // 雨刷器3档
};

typedef std::map<int, bool> ActionEffect; // 受影响的按键位置和对应的新状态

namespace Ui {
class ETS2KeyBinderWizard;
}

class ETS2KeyBinderWizard : public QWizard {
    Q_OBJECT

public:
    explicit ETS2KeyBinderWizard(QWidget* parent = nullptr);
    ~ETS2KeyBinderWizard();

    QStringList getDeviceNameGameList();

    void oneKeyBind(BindingType bindingType, const QString& message);
    void multiKeyBind(std::map<BindingType, ActionEffect> actionEffectMap);

    std::vector<BigKey> getMultiKeyState(const QString& title, const QStringList& messages);

signals:
    void keyStateUpdate_Signal(BigKey& keyState); // 更新按键状态信号

public slots:
    void modifyControlsSii_Slot(BindingType bindingType, ActionEffect actionEffect);

private slots:

    void on_comboBox_activated(int index);

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void on_comboBox_3_activated(int index);

    void on_comboBox_2_activated(int index);

    void on_checkBox_3_clicked(bool checked);

    void on_pushButton_16_clicked();

    void on_pushButton_5_clicked();

    void on_pushButton_6_clicked();

    void on_pushButton_7_clicked();

    void on_pushButton_8_clicked();

    void on_pushButton_9_clicked();

    void on_pushButton_10_clicked();

    void on_pushButton_11_clicked();

    void on_pushButton_12_clicked();

    void on_pushButton_13_clicked();

    void on_pushButton_14_clicked();

    void on_pushButton_15_clicked();

    void on_pushButton_17_clicked();

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

    ShowKeyState* showKeyState = nullptr; // 显示按键状态窗口
    QTimer* timer = nullptr;              // 定时器

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
