# -*- coding:utf-8 -*-
import random
import subprocess
import time
import os, sys
from utils.paddle_opt import paddle_ocr_obj
from datetime import datetime

# 将主目录加入环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)

# app名称
app_name = {
    "ugc": "抖音",
    "ugc_lite": "抖音极速版",
    "article_lite": "头条极速版",
    "kuaishou": "快手",
    "dragon_read": "番茄小说"
    # "wk_browser": "悟空浏览器"
}
# app package 名称 用于关闭应用
app_package_name = {
    "ugc": "com.ss.android.ugc.aweme",
    "ugc_lite": "com.ss.android.ugc.aweme.lite",
    "article_lite": "com.ss.android.article.lite",
    "kuaishou": "com.kuaishou.nebula",
    "dragon_read": "com.dragon.read",
    "wk_browser": "com.cat.readall"
}
# app activity 名称 用于打开应用
app_activity_name = {
    "ugc": "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity",
    "ugc_lite": "com.ss.android.ugc.aweme.lite/com.ss.android.ugc.aweme.splash.SplashActivity",
    "article_lite": "com.ss.android.article.lite/.activity.SplashActivity",
    "kuaishou": "com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity",
    "dragon_read": "com.dragon.read/.pages.splash.SplashActivity",
    "wk_browser": "com.cat.readall/.activity.BrowserMainActivity"
}

device_passwd = {
    "wxk": "910729",
    "fl": "191729",
    "cpc": "2325",
    "cpc2": "123456"
}

device_user = {
    "wxk": ["192.168.101.101:5555", "192.168.31.123:5555", "QKXUT20329000108"],
    "fl": ["192.168.101.100:5555", "94P0220C01001100"],
    "cpc": ["192.168.101.103:5555", "192.168.31.212:5555"],
    "cpc2": ["192.168.101.104:5555", "192.168.31.227:5555"]
}

online_id_list = ["192.168.101.100:5555", "192.168.101.101:5555", "192.168.31.123:5555", "192.168.31.212:5555",
                  "192.168.31.227:5555", "d2b75f1d"]
offline_id_list = ["192.168.101.100:5555", "192.168.31.124:5555"]
# offline_id_list = []
device_id_list = list(set(online_id_list) - set(offline_id_list))


def print_help_text(device_id, help_text, current_step=''):
    text = "[设备：%s] %s 执行步骤：%s %s" % (device_id, datetime.now().strftime("%H:%M:%S"), current_step, help_text)
    print(text)


# 执行系统命令
def opt_sys_command(command, sleep_time=1):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    result = p.communicate()[0].decode()
    time.sleep(1)
    return result.split('\r\n')


def get_app_activity_name():
    # 获取当前app的activity name
    command = "shell dumpsys window | findstr mCurrentFocus"
    command = "adb shell dumpsys activity activities | findstr 'Run'"
    # 如果上面报错permission deny 有可能不是真的activity名称 然后查找LAUNCHER
    command = "adb shell dumpsys package com.dragon.read"


# 获取目前所有device_id
def get_all_device_id():
    global offline_id_list
    p = opt_sys_command("adb devices")
    device_id_list = []
    for i in p[1:]:
        if i:
            device_id_list.append(i.split('\t')[0])
    device_list = list(set(device_id_list) - set(offline_id_list))
    return device_list


# 重启adb server
def reboot_adb():
    global device_id_list
    for i in device_id_list:
        command = "adb connect " + i
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    device_id_list_current = get_all_device_id()
    if len(device_id_list_current) == 0:
        command = "tasklist | findstr adb"
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.stdout.readlines()
        pid = [i for i in out[0].decode().split(' ') if i][1]
        command = "taskkill /f /pid " + pid
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for i in device_id_list:
            command = "adb connect " + i
            os.system(command)
        # 获取连接的device_list
    connected_device_id_list = get_all_device_id()
    no_device_id_list = set(device_id_list) - set(connected_device_id_list)
    print(
        "已连接%s设备：%s" % (len(connected_device_id_list), " ".join(connected_device_id_list))
    )
    print(
        "未连接%s设备：%s" % (len(no_device_id_list), " ".join(no_device_id_list))
    )
    if len(connected_device_id_list) == 0:
        sys.exit(-1)


reboot_adb()

CurrentDeviceList = get_all_device_id()


def get_user_passwd(device_id):
    # 获取用户锁屏密码
    user = ''
    for k, v in device_user.items():
        if device_id in v:
            user = k
            break
    if not user:
        return ''
    if user not in device_passwd.keys():
        return ''
    return device_passwd[user]


# 按键
def press_key(device_id, key):
    '''
    手机按键
    :param device_id: 设备id
    :param key: 按键
    :return:
    3HOME键  4返回键  5打开拨号应用 6挂断电话 24增加音量 25降低音量 26电源键 27拍照（需要在相机应用里）
    64打开浏览器 82菜单键 85播放/暂停 86停止播放 87播放下一首 88播放上一首 122移动光标到行首或列表顶部
    123移动光标到行末或列表底部 126恢复播放 127暂停播放 164静音 176打开系统设置 187切换应用 207打开联系人
    208打开日历 209打开音乐 210打开计算器 220降低屏幕亮度 221提高屏幕亮度
    223系统休眠 224点亮屏幕 231打开语音助手 276如果没有wakelock让系统休眠
    '''
    command = "adb -s " + device_id + " shell input keyevent " + str(key)
    opt_sys_command(command)


# 输入文字
def input_text(device_id, text):
    command = "adb -s " + device_id + " shell input text " + str(text)
    opt_sys_command(command)


# 点亮屏幕
def light_screen(device_id):
    press_key(device_id, 224)


# 解锁手机
def unlock_device(device_id):
    print_help_text(device_id, "点亮屏幕")
    light_screen(device_id)
    print_help_text(device_id, "上滑屏幕")
    up_short_swipe(device_id)
    time.sleep(1)
    print_help_text(device_id, "输入密码")
    input_text(device_id, get_user_passwd(device_id))


# 熄屏
def shut_screen(device_id):
    press_key(device_id, 223)


# 按电源键
def press_power(device_id):
    press_key(device_id, 26)


# 返回建
def press_back(device_id):
    press_key(device_id, 4)


# 禁音
def mute(device_id):
    press_key(device_id, 164)


# 截屏
def screen_cap(device_id):
    png_name = "/sdcard/DCIM/screen_" + device_id.split(":")[0] + ".png"
    command = "adb -s %s shell screencap %s" % (device_id, png_name)
    opt_sys_command(command)
    time.sleep(0.5)
    return png_name


# 拷贝图片
def screen_pull(device_id, png_name):
    local_png = os.path.join(BASE_DIR, "media", png_name.split('/')[-1])
    command = "adb -s " + device_id + " pull %s %s" % (png_name, local_png)
    opt_sys_command(command)
    return local_png


# 查找屏幕中某个字的位置
def find_screen_text_position(device_id, text, top_normal_bottom='normal'):
    # 截屏
    png_name = screen_cap(device_id)
    # 拷贝
    local_png = screen_pull(device_id, png_name)
    # 识别
    if top_normal_bottom == "normal":
        result = paddle_ocr_obj.detect(local_png)
    if top_normal_bottom == "top":
        result = paddle_ocr_obj.detect_top(local_png)
    if top_normal_bottom == 'bottom':
        result = paddle_ocr_obj.detect_bottom(local_png)
    status = False
    if not result:
        return status, [], []
    box = []
    for i in result:
        if i[1][0].find(text) >= 0:
            status = True
            box = i[0]
            break
    return status, box, result


# 查找某个功能文字下的按钮
def find_screen_text_button_position(device_id, text, button_text, top_normal_bottom='normal'):
    # 先在屏幕上查询该功能的文字
    status, box, result = find_screen_text_position(device_id, text, top_normal_bottom=top_normal_bottom)
    if status:
        # 如果找到了 则找下面的按钮
        y_ad = box[0][1]
        for line in result:
            # 如果找到了该位置
            if line[1][0].find(button_text) >= 0 and line[0][0][1] >= (y_ad - 80) and line[0][0][1] <= (y_ad + 80):
                x, y = int((line[0][0][0] + line[0][1][0]) / 2), int((line[0][0][1] + line[0][1][1]) / 2)
                return True, (x, y)
    return False, ()


# 查看本页某个按钮
def find_screen_by_result(result, text):
    for i in result:
        if i[1][0].find(text) >= 0:
            x = int((i[0][0][0] + i[0][1][0]) / 2)
            y = int((i[0][1][1] + i[0][2][1]) / 2)
            position = (x, y)
            return position
    return ()


# 点击
def tap(device_id, position):
    '''
    屏幕点击
    :param device_id: 设备id
    :param position: (x, y) 元组
    :return:
    '''
    x, y = position
    command = "adb -s " + device_id + " shell input tap " + str(x) + " " + str(y)
    opt_sys_command(command)


# 滑动
def swipe(device_id, position_start, position_end, time_period=150):
    x_s, y_s = position_start
    x_e, y_e = position_end
    command = "adb -s %s shell input swipe %s %s %s %s %s" % (device_id, x_s, y_s, x_e, y_e, time_period)
    opt_sys_command(command)


# 上滑 短程
def up_short_swipe(device_id):
    swipe(device_id, (40, 2000), (40, 1400))


# 长上滑
def up_long_swipe(device_id):
    swipe(device_id, (40, 2000), (40, 550), 550)


# 下滑 短程
def down_short_swipe(device_id):
    swipe(device_id, (40, 1600), (40, 2000))


# 长下滑
def down_long_swipe(device_id):
    swipe(device_id, (40, 550), (40, 2000), 550)


# 启动app
def start_app(device_id, app):
    global app_activity_name
    content = "开始启动" + app_name[app]
    print_help_text(device_id, content)
    command = "adb -s " + device_id + " shell  am start " + app_activity_name[app]
    opt_sys_command(command)


# 关闭app
def shut_app(device_id, app):
    global app_package_name
    command = "adb -s " + device_id + " shell am force-stop " + app_package_name[app]
    opt_sys_command(command)


def get_phone_wh(device_id):
    command = "adb -s " + device_id + " shell wm size"
    lines = opt_sys_command(command)
    wh = lines[0].split(':')[-1].strip().split("x")
    wh = (wh[0], wh[1])
    return wh


def get_random_time(min=1, max=3):
    # 随机生产事件间隔
    return random.randint(min, max)


def unclock_all_devices():
    from concurrent.futures import ThreadPoolExecutor, wait
    # 解锁所有设备
    max_workers = len(CurrentDeviceList)
    executor_unlock = ThreadPoolExecutor(max_workers=max_workers)
    unlock_task_list = []
    for device_id in CurrentDeviceList:
        print_help_text(device_id, "解锁设备！")
        unlock_task_list.append(
            executor_unlock.submit(unlock_device, device_id)
        )
    wait(unlock_task_list)


if __name__ == "__main__":
    # reboot_adb()
    # unlock_device("192.168.101.100:8888")
    device_id = "192.168.101.104:5555"
    stats, position = find_screen_text_button_position(device_id, "已成功领取", "已成功领取")
    # get_phone_wh(device_id)
