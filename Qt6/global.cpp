#include <QString>
#include <global.h>

// 参考开源项目：https://github.com/InsistonTan/KeyMappingsTool

QList<DiDeviceInfo> diDeviceList;

// DirectInput 回调函数，用于列出所有连接的游戏控制器设备
BOOL CALLBACK EnumDevicesCallback(const DIDEVICEINSTANCE* pdidInstance, VOID* pContext) {
    DiDeviceInfo deviceInfo;
    deviceInfo.name = QString::fromWCharArray(pdidInstance->tszProductName).toStdString();
    deviceInfo.guidInstance = pdidInstance->guidInstance;
    diDeviceList.append(deviceInfo);
    return DIENUM_CONTINUE;
}
