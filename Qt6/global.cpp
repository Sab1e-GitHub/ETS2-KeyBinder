#include <QString>
#include <global.h>

// 参考开源项目：https://github.com/InsistonTan/KeyMappingsTool

QList<DiDeviceInfo> diDeviceList;

std::string guidToString(const GUID& guid) {
    char buffer[39]; // GUID字符串固定为38个字符 + 终止符
    snprintf(buffer, sizeof(buffer), "(%08lX)", guid.Data1);
    return std::string(buffer);
}

// DirectInput 回调函数，用于列出所有连接的游戏控制器设备
BOOL CALLBACK EnumDevicesCallback(const DIDEVICEINSTANCE* pdidInstance, VOID* pContext) {
    DiDeviceInfo deviceInfo;
    deviceInfo.name = QString::fromWCharArray(pdidInstance->tszProductName).toStdString();
    deviceInfo.name += guidToString(pdidInstance->guidProduct);
    deviceInfo.guidInstance = pdidInstance->guidInstance;
    diDeviceList.append(deviceInfo);
    return DIENUM_CONTINUE;
}
