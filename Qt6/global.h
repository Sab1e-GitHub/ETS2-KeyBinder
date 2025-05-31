#ifndef GLOBAL_H
#define GLOBAL_H

// 参考开源项目：https://github.com/InsistonTan/KeyMappingsTool

#include <QList>
#include <dinput.h>
#include <string>

#define DINPUT_MAX_BUTTONS 128 // DirectInput 最大按键数

struct DiDeviceInfo {
    std::string name;
    GUID guidInstance;
};

extern QList<DiDeviceInfo> diDeviceList; // 设备列表

BOOL CALLBACK EnumDevicesCallback(const DIDEVICEINSTANCE* pdidInstance, VOID* pContext);

#endif // GLOBAL_H
