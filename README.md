# ETS2 KeyMapper
欧洲卡车模拟2 特殊按键绑定工具

**由于鄙人时间紧张，因此写了个命令行版本的，如果哪位大佬可以提供UI版本，感激不尽！**

## 简述：

举个例子：如果我们的左转向灯外设是开关型触发的，而不是像键盘一样的是按钮型触发（分不清开关和按钮的请自行搜索），那么我们在欧卡2的设置中就无法绑定了，因为它在设置中只提供了按钮型触发。

我看到网上很多人的做法是去写一个中间层去映射欧卡内给出的按键，比如说开关打开时，去按一下“[”键就可以打开左转向灯了，然后开关关闭时再按一下就可以关闭左转向灯了。

其实鄙人前段时间就是这么做的，软件上传到GItHub了但是没有公开，因为这样做有很多问题，例如灯光组合它只能一下一下按“L”键，这样你的灯光就会来回闪。（伏啦史棒）

但是实际上欧卡2是支持绑定开关型触发的，只不过在游戏内无法修改，而是可以通过修改配置文件来实现，具体文件位置在：
`C:\Users\<User Name>\Documents\Euro Truck Simulator 2\steam_profiles\<配置ID文件夹>\controls.sii`。

修改方法例子：

红框内的内容就是按键的映射
![image](https://github.com/user-attachments/assets/ced9f5cb-b629-4aa2-aaa1-6d4b18561b69)



那么我们就可以通过修改配置文件来绑定开关，从而控制欧卡2内的左转向灯。
但是手动修改配置文件实在是太麻烦了，所以写了这个程序用于解决此问题。

## 用户须知：

1. 此软件使用时需要关闭游戏，否则修改无效。
原因：经过我的测试，欧卡2关于此配置文件的控制逻辑是（可能不准确）：当游戏打开时，读取此文件然后加载到内存，每次你打开设置界面，
然后修改按键，都是在内存中修改的，当你退出设置界面，你修改后的配置会从内存中保存到此文件中（直接覆盖！）。
1. 你需要知道零基索引和一基索引，当你使用自动绑定和手动绑定时，自动显示和手动输入的都是零基索引，因为欧卡2在设置页面就是零基索引。零基索引：从0开始的索引。一基索引：从1开始的索引。
1. 自动灯光绑定时，绑定远光灯是对应的游戏内的“灯光喇叭”按钮，这是为了适配我的设备所以这么做的。
1. 务必分清什么是按钮什么是开关。
1. 你需要知道你的游戏控制器是在哪一个“输入类型”
![Screenshot 2024-11-08 201052](https://github.com/user-attachments/assets/a3525e51-a98f-4415-aed9-53c3a86d3119)
![image](https://github.com/user-attachments/assets/48abe1d6-30a5-4661-b8f8-701a048a2f7f)


## 当前功能：

1. 支持自动检测按键进行绑定
1. 支持手动绑定

## 目前可绑定：
1. 灯光关闭开关
1. 示宽灯开关
1. 近光灯开关
1. 远光灯开关
1. 灯光喇叭开关
1. 雨刮关闭开关
1. 雨刮一档开关
1. 雨刮二挡开关
1. 雨刮三挡开关
1. 左转向灯开关
1. 右转向灯开关
