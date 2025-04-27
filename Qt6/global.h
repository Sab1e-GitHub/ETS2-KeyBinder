#ifndef GLOBAL_H
#define GLOBAL_H

#include <QList>
#include <dinput.h>
#include <string>

struct DiDeviceInfo {
    std::string name;
    GUID guidInstance;
};

extern QList<DiDeviceInfo> diDeviceList; // 设备列表

BOOL CALLBACK EnumDevicesCallback(const DIDEVICEINSTANCE* pdidInstance, VOID* pContext);

#endif // GLOBAL_H
