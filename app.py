import pygame
import os
import time
from enum import Enum
from pathlib import Path
from datetime import datetime
import re
import shutil

# 欧卡2 设置    “摇杆 Button0” 0基索引
# 欧卡2 配置文件 “joy.b1”      1基索引
# pygame Button_Index         0基索引

# 定义枚举类型
class BindingType(Enum):
    lightoff = 1
    lighthorn = 2
    wipers0 = 3
    wipers1 = 4
    wipers2 = 5
    wipers3 = 6
    lightpark = 7
    lighton = 8
    hblight = 9
    lblinkerh = 10
    rblinkerh = 11

    @staticmethod
    def modify_controls_sii(controls_file, binding_type, ets2_str):
        """
        修改 controls.sii 文件，只替换与传入的 binding_type 相应的行。
        """
        if not controls_file.exists():
            raise FileNotFoundError(f"{controls_file} 文件未找到")

        # 替换规则字典，根据 binding_type 动态生成替换字符串
        replace_rules = {
            BindingType.lightoff: r"mix lightoff `.*?semantical\.lightoff\?0`",
            BindingType.lighthorn: r"mix lighthorn `.*?semantical\.lighthorn\?0`",
            BindingType.wipers0: r"mix wipers0 `.*?semantical\.wipers0\?0`",
            BindingType.wipers1: r"mix wipers1 `.*?semantical\.wipers1\?0`",
            BindingType.wipers2: r"mix wipers2 `.*?semantical\.wipers2\?0`",
            BindingType.wipers3: r"mix wipers3 `.*?semantical\.wipers3\?0`",
            BindingType.lightpark: r"mix lightpark `.*?semantical\.lightpark\?0`",
            BindingType.lighton: r"mix lighton `.*?semantical\.lighton\?0`",
            BindingType.hblight: r"mix hblight `.*?semantical\.hblight\?0`",
            BindingType.lblinkerh: r"mix lblinkerh `.*?semantical\.lblinkerh\?0`",
            BindingType.rblinkerh: r"mix rblinkerh `.*?semantical\.rblinkerh\?0`",
        }

        if binding_type not in replace_rules:
            print(f"无效的绑定类型: {binding_type}")
            return

        # 打开文件并读取内容
        with controls_file.open('r', encoding='utf-8') as file:
            lines = file.readlines()

        modified_lines = []
        modified = False

        # 获取替换规则
        pattern = replace_rules[binding_type]
        replacement = f"mix {binding_type.name} `{ets2_str} | semantical.{binding_type.name}?0`"

        # 逐行检查并修改文件内容
        for line in lines:
            if re.search(pattern, line):
                print(f"匹配到: {line.strip()}")  # 调试输出
                line = re.sub(pattern, replacement, line)
                modified = True
            modified_lines.append(line)

        # 如果有修改，写回文件
        if modified:
            with controls_file.open('w', encoding='utf-8') as file:
                file.writelines(modified_lines)
            print(f"成功修改文件：{controls_file}")
        else:
            print("未检测到需要修改的内容")

# 这个joy index不是用于按键检测的索引，是欧卡2多个控制器的索引
ets2_joy_index = 0

seleceted_profile = ""


def backup_file(file_path):
    # 转换为 Path 对象
    original_file = Path(file_path)
    
    # 检查原始文件是否存在
    if not original_file.exists():
        print(f"文件 {file_path} 不存在，无法备份。")
        return

    # 生成备份文件路径
    backup_file_path = original_file.with_suffix(original_file.suffix + '.bak')

    # 复制文件，直接覆盖备份文件（如果存在）
    shutil.copy2(original_file, backup_file_path)
    
    print(f"文件已备份至: {backup_file_path}")

# 清空控制台
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')




    # 查找最近修改的配置文件
def find_latest_profile_folder(profiles_path):
    folders = [f for f in profiles_path.iterdir() if f.is_dir()]
    if not folders:
        raise FileNotFoundError("未找到任何配置配置文件")
    
    # 根据修改时间排序，选择最近的配置文件
    latest_folder = max(folders, key=lambda f: f.stat().st_mtime)
    return latest_folder

# 检测控制器的持续按键
def detect_joystick_buttons(joystick):
    #print("\n正在检测控制器的按钮状态...\n")
    time.sleep(0.5)
    pressed_buttons_list = []
    pygame.event.pump()  # 处理事件队列，确保按钮状态更新

    for button_id in range(joystick.get_numbuttons()):
        if joystick.get_button(button_id):  # 如果按钮被按下
            #print(f"按钮 {button_id} 持续按下")
            pressed_buttons_list.append(button_id)
    
    return pressed_buttons_list


def pygame_button_index_convert_to_ets2_str(button_index):
    """
    将Pygame的按钮索引转换为ETS2的按键字符串表示。
    """
    return f"joy{ets2_joy_index}.b{button_index}?0" if ets2_joy_index != 0 else f"joy.b{button_index}?0"

def bind_button(binding_type, button_index):
    """
    根据绑定类型和按钮索引修改配置文件中的相应条目。
    """
    global seleceted_profile
    ets2_str = pygame_button_index_convert_to_ets2_str(button_index)

    # 调用 modify_controls_sii 函数进行特定的替换
    BindingType.modify_controls_sii(seleceted_profile, binding_type, ets2_str)

def auto_bind_light(joystick):
    last_pressed_buttons_lsit=[]
    current_pressed_buttons_list=[]

    clear_console()
    print("灯光组合绑定 (1/4)\n\n现在请你将灯光全部关闭，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态

    
    print("灯光组合绑定 (2/4)\n\n现在请你仅打开示宽灯，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    lightoff_button_index_set=set(last_pressed_buttons_lsit) - set(current_pressed_buttons_list)    #刚刚关闭的就是灯光关闭按钮
    parkinglight_button_index_set= set(current_pressed_buttons_list) - set(last_pressed_buttons_lsit)   #与此同时打开的就是示宽灯按钮


    
    print("灯光组合绑定 (3/4)\n\n现在请你仅打开近光灯，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = current_pressed_buttons_list
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    lowbeam_button_index_set =  set(current_pressed_buttons_list) - set(last_pressed_buttons_lsit) #刚刚打开的就是近光灯按钮

    

    print("灯光组合绑定 (4/4)\n\n现在请你仅打开远光灯，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = current_pressed_buttons_list
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    
    highbeam_button_index_set = set(current_pressed_buttons_list) - set(last_pressed_buttons_lsit)  #刚刚打开的就是远光灯按钮



    print("自动检测结果：")
    if(lightoff_button_index_set==set())or(parkinglight_button_index_set==set())or (lowbeam_button_index_set==set())or (highbeam_button_index_set==set()):
        input("检测失败，按下回车返回上级菜单。")
    else:
        lightoff_button_index=list(lightoff_button_index_set)[0]+1
        parkinglight_button_index=list(parkinglight_button_index_set)[0]+1
        lowbeam_button_index=list(lowbeam_button_index_set)[0]+1
        highbeam_button_index=list(highbeam_button_index_set)[0]+1


        print(f"灯光关闭按钮:   摇杆 Button{lightoff_button_index-1}")
        print(f"示宽灯按钮:     摇杆 Button{parkinglight_button_index-1}")
        print(f"近光灯按钮:     摇杆 Button{lowbeam_button_index-1}")
        print(f"远光灯按钮:     摇杆 Button{highbeam_button_index-1}")

        while(True):
            lb_selection = input("\n是否确认绑定？\n确认=1 取消=0\n")
            if lb_selection == "1":
                
                bind_button(BindingType.lightoff,lightoff_button_index)
                bind_button(BindingType.lightpark,parkinglight_button_index)
                bind_button(BindingType.lighton,lowbeam_button_index)
                bind_button(BindingType.lighthorn,highbeam_button_index)
                break
            elif lb_selection == "0":
                break
            else:
                print("无效输入！")
                pass

def auto_bind_wipers(joystick):
    last_pressed_buttons_lsit=[]
    current_pressed_buttons_list=[]

    clear_console()
    print("雨刮器组合绑定 (1/4)\n\n现在请你将雨刮器关闭，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态

    
    print("雨刮器组合绑定 (2/4)\n\n现在请你打开雨刮器一档，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    wipers_0_button_index_set=set(last_pressed_buttons_lsit) - set(current_pressed_buttons_list)    #刚刚关闭的就是灯光关闭按钮
    wipers_1_button_index_set= set(current_pressed_buttons_list) - set(last_pressed_buttons_lsit)   #与此同时打开的就是示宽灯按钮


    
    print("雨刮器组合绑定 (3/4)\n\n现在请你打开雨刮器二档，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = current_pressed_buttons_list
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    wipers_2_button_index_set =  set(current_pressed_buttons_list) - set(last_pressed_buttons_lsit) #刚刚打开的就是近光灯按钮

    

    print("雨刮器组合绑定 (4/4)\n\n现在请你打开雨刮器三档，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = current_pressed_buttons_list
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    
    wipers_3_button_index_set = set(current_pressed_buttons_list) - set(last_pressed_buttons_lsit)  #刚刚打开的就是远光灯按钮



    print("自动检测结果：")
    if(wipers_0_button_index_set==set())or(wipers_1_button_index_set==set())or (wipers_2_button_index_set==set())or (wipers_3_button_index_set==set()):
        input("检测失败，按下回车返回上级菜单。")
    else:
        wipers_0_button_index=list(wipers_0_button_index_set)[0]+1
        wipers_1_button_index=list(wipers_1_button_index_set)[0]+1
        wipers_2_button_index=list(wipers_2_button_index_set)[0]+1
        wipers_3_button_index=list(wipers_3_button_index_set)[0]+1


        
        print(f"雨刮关闭按钮:   摇杆 Button{wipers_0_button_index-1}")
        print(f"雨刮器一档按钮: 摇杆 Button{wipers_1_button_index-1}")
        print(f"雨刮器二挡按钮: 摇杆 Button{wipers_2_button_index-1}")
        print(f"雨刮器三挡按钮: 摇杆 Button{wipers_3_button_index-1}")

        while(True):
            lb_selection = input("\n是否确认绑定？\n确认=1 取消=0\n")
            if lb_selection == "1":
                
                bind_button(BindingType.wipers0,wipers_0_button_index)
                bind_button(BindingType.wipers1,wipers_1_button_index)
                bind_button(BindingType.wipers2,wipers_2_button_index)
                bind_button(BindingType.wipers3,wipers_3_button_index)
                break
            elif lb_selection == "0":
                break
            else:
                print("无效输入！")
                pass


def manually_bind_menu(joystick):
    while(True):
        print("=====手动绑定菜单=====\n（注意：手动绑定按钮在输入索引后立即绑定，不会重复提示确认！）\n1.绑定灯光关闭按钮\n2.绑定示宽灯按钮\n3.绑定近光灯按钮\n4.绑定远光灯按钮")
        print("5.绑定灯光喇叭按钮\n6.绑定雨刮关闭按钮\n7.绑定雨刮一档按钮\n8.绑定雨刮二挡按钮\n9.绑定雨刮三挡按钮\n10.绑定左转向灯按钮")
        print("11.绑定右转向灯按钮\n0.返回主菜单")
        print("=====================")
        selection = input("请输入选择：\n")
        clear_console()
        if selection == "1":
            button_index = input("绑定灯光关闭按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.lightoff,int(button_index)+1)       # 配置文件是1基索引，因此+1
                pass
        elif selection == "2":
            button_index = input("绑定示宽灯按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.lightpark,int(button_index)+1)
                pass
        elif selection == "3":
            button_index = input("绑定近光灯按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.lighton,int(button_index)+1)
                pass
        elif selection == "4":
            button_index = input("绑定远光灯按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.hblight,int(button_index)+1)
                pass
        elif selection == "5":
            button_index = input("绑定灯光喇叭按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.lighthorn,int(button_index)+1)
                pass
        elif selection == "6":
            button_index = input("绑定雨刮器关闭按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.wipers0,int(button_index)+1)
                pass
        elif selection == "7":
            button_index = input("绑定雨刮器一档按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.wipers1,int(button_index)+1)
                pass
        elif selection == "8":
            button_index = input("绑定雨刮器二档按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.wipers2,int(button_index)+1)
                pass
        elif selection == "9":
            button_index = input("绑定雨刮器三挡按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.wipers3,int(button_index)+1)
                pass
        elif selection == "10":
            button_index = input("绑定左转向灯按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.lblinkerh,int(button_index)+1)
                pass
        elif selection == "11":
            button_index = input("绑定右转向灯按钮\n如需取消，请不要输入任何内容然后按下回车。\n请输入按钮索引数值（0~65535）：")
            if(button_index==""):
                pass
            elif not button_index.isdigit():
                print("=====非法输入！=====")
            elif not int(button_index)<=65535 and not int(button_index)>=0:
                print("=====非法输入！=====")
            else:
                print(f"按钮：Button{button_index} 绑定成功！")
                bind_button(BindingType.rblinkerh,int(button_index)+1)
                pass
        elif selection == "0":
            break

        else:
            print("无效输入！")
            time.sleep(2)  # 等待2秒后重新显示菜单


        
        

    



def auto_bind_left_blinker(joystick):
    last_pressed_buttons_lsit=[]
    current_pressed_buttons_list=[]

    clear_console()
    print("左转向灯绑定 (1/2)\n\n现在请你将左转向灯打开，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态

    clear_console()
    print("左转向灯绑定 (2/2)\n\n现在请你将左转向灯关闭，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    lblink_index_set =set(last_pressed_buttons_lsit) - set(current_pressed_buttons_list)
    print("自动检测结果：")
    if(lblink_index_set ==set()):
        input("检测失败，按下回车返回上级菜单。")
    else:
        lblink_index = list(lblink_index_set)[0]+1
        print(f"左转向灯按钮：摇杆 Button{lblink_index-1}")

        while(True):
            lb_selection = input("\n是否确认绑定？\n确认=1 取消=0\n")
            if lb_selection == "1":
                bind_button(BindingType.lblinkerh,lblink_index)
                break
            elif lb_selection == "0":
                break
            else:
                print("无效输入！")
                pass

def auto_bind_right_blinker(joystick):
    last_pressed_buttons_lsit=[]
    current_pressed_buttons_list=[]

    clear_console()
    print("右转向灯绑定 (1/2)\n\n现在请你将右转向灯打开，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    last_pressed_buttons_lsit = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态

    clear_console()
    print("右转向灯绑定 (2/2)\n\n现在请你将右转向灯关闭，然后按下回车。\n")
    input("（请不要调整其他开关的状态）")
    current_pressed_buttons_list = detect_joystick_buttons(joystick)  # 调用函数来检测控制器按钮状态
    rblink_index_set =set(last_pressed_buttons_lsit) - set(current_pressed_buttons_list)
    print("自动检测结果：")
    if(rblink_index_set ==set()):
        input("检测失败，按下回车返回上级菜单。")
    else:
        rblink_index = list(rblink_index_set)[0]+1
        print(f"右转向灯按钮：摇杆 Button{rblink_index-1}")

        while(True):
            lb_selection = input("\n是否确认绑定？\n确认=1 取消=0\n")
            if lb_selection == "1":
                bind_button(BindingType.rblinkerh,rblink_index)
                break
            elif lb_selection == "0":
                break
            else:
                print("无效输入！")
                pass

def list_folders_with_modification_dates(directory):
    """
    列出目录下的所有配置文件及其最后修改日期。
    """

    # 确保路径存在
    if not directory.exists():
        print(f"路径 {directory} 不存在!")
        return []
    
    # 获取目录下的所有子目录
    folders = [f for f in directory.iterdir() if f.is_dir()]
    
    # 如果目录为空，返回
    if not folders:
        print(f"{directory} 目录下没有配置文件.")
        return []
    
    # 打印每个配置文件及其最后修改时间
    folder_info = []
    for folder in folders:
        # 获取配置文件最后修改时间
        mtime = os.path.getmtime(folder)
        last_modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        folder_info.append((folder.name, last_modified))
        print(f"检索到：{folder}")
    
    return folder_info

def select_user_profile():
    global seleceted_profile
    # 定义两个路径
    steam_profiles = Path.home() / "Documents" / "Euro Truck Simulator 2" / "steam_profiles"
    profiles = Path.home() / "Documents" / "Euro Truck Simulator 2" / "profiles"
    print("开始检索用户配置文件...")
    # 列出steam_profiles路径下的配置文件
    print("\nSteam Profiles:")
    steam_folders = list_folders_with_modification_dates(steam_profiles)
    
    # 列出profiles路径下的配置文件
    print("\nProfiles:")
    profile_folders = list_folders_with_modification_dates(profiles)
    
    # 合并两个配置文件列表
    all_folders = steam_folders + profile_folders
    
    if not all_folders:
        print("没有找到任何配置文件！")
        return
    
    # 打印所有配置文件，并让用户选择
    print("\n请选择一个配置文件:")
    for idx, (folder_name, mod_time) in enumerate(all_folders, start=1):
        print(f"{idx}. {folder_name} (最后修改时间: {mod_time})")
    
    # 获取用户的选择
    try:
        choice = int(input(f"请输入配置文件编号 (1-{len(all_folders)}): "))
        if 1 <= choice <= len(all_folders):
            selected_folder = all_folders[choice - 1][0]
            print(f"已选择的配置文件: {selected_folder}")
            if choice <= len(steam_folders):
                seleceted_profile = steam_profiles / selected_folder / "controls.sii"
            else:
                seleceted_profile = profiles / selected_folder / "controls.sii"
            print(f"配置文件完整路径：{seleceted_profile}")
            backup_file(seleceted_profile)
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入一个有效的数字！")

def select_joystick():
    # 初始化Pygame
    pygame.init()

    # 获取所有连接的游戏控制器数量
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("没有检测到游戏控制器")
        return None  # 没有控制器时返回 None

    # 显示所有连接的游戏控制器名称
    print("检测到以下游戏控制器：")
    joystick_list = []
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joystick_list.append(joystick.get_name())
        print(f"{i + 1}. {joystick.get_name()}")
    
    # 让用户选择控制器
    try:
        selected_index = int(input("请选择一个控制器 (输入数字): ")) - 1
        if selected_index < 0 or selected_index >= joystick_count:
            print("选择无效")
            return None  # 返回 None 表示选择无效
        else:
            selected_joystick = joystick_list[selected_index]
            print(f"你选择的控制器是: {selected_joystick}")
            # 获取该控制器对象
            joystick = pygame.joystick.Joystick(selected_index)
            joystick.init()
            print("设备连接成功！")
            return joystick
    except ValueError:
        print("请输入有效的数字")
        return None  # 如果输入无效，返回 None

def select_ets2_joystick():
    
    while(True):
        user_input = input("\n在欧卡2的'设置->控制->输入类型'处有多个下拉栏\n请选择你的游戏控制器是在第几个下拉栏\n（从0开始数，默认为0）\n请输入: ")
    
        if user_input.isdigit():
            ets2_joy_index = user_input
            print(f"已设置{ets2_joy_index}")
            break
        elif user_input == "":
            ets2_joy_index = 0
            print(f"已设置{ets2_joy_index}")
            break
        else:
            print("只能输入数字！")

def menu(joystick):
    while True:
        # clear_console()
        
        print("\n=====主菜单=====\n(请不要打开游戏，否则绑定无效)\n1.自动绑定灯光组合\n2.自动绑定雨刮器组合\n3.自动绑定左转向灯\n4.自动绑定右转向灯\n5.手动绑定\n0.退出程序\n================")
        selection = input("请输入选择：")  # 将输入转换为整数
        clear_console()
        
        if selection == "1":
            auto_bind_light(joystick)
        elif selection == "2":
            auto_bind_wipers(joystick)
        elif selection == "3":
            auto_bind_left_blinker(joystick)
        elif selection == "4":
            auto_bind_right_blinker(joystick)
        elif selection == "5":
            manually_bind_menu(joystick)
        elif selection == "0":
            print("程序退出")
            exit()  # 正确使用 exit() 退出程序
        else:
            print("无效输入！")
            time.sleep(2)  # 等待2秒后重新显示菜单



def main():
    try:
        while True:
            clear_console()
            joystick = select_joystick()
            if joystick:
                select_user_profile()
                select_ets2_joystick()
                menu(joystick)
    except KeyboardInterrupt:
        print("\n程序已退出")


if __name__ == "__main__":
    main()
