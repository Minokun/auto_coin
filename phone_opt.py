# -*- coding:utf-8 -*-
import random
import subprocess
import time

# app名称
app_name = {
    "ugc": "抖音",
    "ugc_lite": "抖音极速版",
    "article_lite": "头条极速版",
    "wk_browser": "悟空浏览器",
    "dragon_read": "番茄小说"

}
# app package 名称 用于关闭应用
app_package_name = {
    "ugc": "com.ss.android.ugc.aweme",
    "ugc_lite": "com.ss.android.ugc.aweme.lite",
    "article_lite": "com.ss.android.article.lite",
    "wk_browser": "com.cat.readall",
    "dragon_read": "com.dragon.read"
}
# app activity 名称 用于打开应用
app_activity_name = {
    "ugc": "com.ss.android.ugc.aweme/com.ss.android.ugc.aweme.main.MainActivity",
    "ugc_lite": "com.ss.android.ugc.aweme.lite/com.ss.android.ugc.aweme.splash.SplashActivity",
    "article_lite": "com.ss.android.article.lite/.activity.SplashActivity",
    "wk_browser": "com.cat.readall/.activity.BrowserMainActivity",
    "dragon_read": "com.dragon.read/.pages.main.MainFragmentActivity"
}


# 多设备装饰器 一定要注意参数顺序要一样
def multiple_device(device_list, time_period=0):
    def _opt(func):
        argv = [i for i in [device_list, time_period] if i]
        for device_id in device_list:
            argv[0] = device_id
            func(*argv)
    return _opt


# 执行系统命令
def opt_sys_command(command, sleep_time=1):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    result = p.communicate()[0].decode()
    time.sleep(sleep_time)
    return result.split('\r\n')


# 获取目前所有device_id
def get_all_device_id():
    p = opt_sys_command("adb devices")
    device_id_list = []
    for i in p[1:]:
        if i:
            device_id_list.append(i.split('\t')[0])
    return device_id_list


CurrentDeviceList = get_all_device_id()

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
    png_name = "/sdcard/DCIM/screen_" + device_id + ".png"
    command = "adb -s %s shell screencap %s" % (device_id, png_name)
    opt_sys_command(command)
    return png_name

# 拷贝图片
def screen_pull(png_name):
    local_png = "media/" + png_name.split('/')[-1]
    command = "adb pull %s %s" % (png_name, local_png)
    opt_sys_command(command)
    return local_png

# 查找屏幕中某个字的位置
def find_screen_text_position(device_id, text):
    from paddle_opt import DetectPic
    paddle_detect = DetectPic()
    # 截屏
    png_name = screen_cap(device_id)
    # 拷贝
    local_png = screen_pull(png_name)
    # 识别
    paddle_detect.detect(local_png)
    status = False
    box = []
    for i in paddle_detect.result:
        if i[1][0].find(text) >= 0:
            status = True
            box = i[0]
            break
    return status, box, paddle_detect.result

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
def swipe(device_id, position_start, position_end, time_period=100):
    x_s, y_s = position_start
    x_e, y_e = position_end
    command = "adb -s %s shell input swipe %s %s %s %s %s" % (device_id, x_s, y_s, x_e, y_e, time_period)
    opt_sys_command(command)


# 上滑 短程
def up_short_swipe(device_id):
    swipe(device_id, (550, 1800), (550, 1300))


# 长上滑
def up_long_swipe(device_id):
    swipe(device_id, (550, 2100), (550, 500), 1000)


# 下滑 短程
def down_short_swipe(device_id):
    swipe(device_id, (550, 1300), (550, 1800))


# 长下滑
def down_long_swipe(device_id):
    swipe(device_id, (550, 500), (550, 2100), 1000)


# 启动app
def start_app(device_id, app):
    global app_activity_name
    print("设备%s 开始启动%s ......" % (device_id, app_name[app]))
    command = "adb -s " + device_id + " shell  am start " + app_activity_name[app]
    opt_sys_command(command)


# 关闭app
def shut_app(device_id, app):
    global app_package_name
    command = "adb -s " + device_id + " shell am force-stop " + app_package_name[app]
    opt_sys_command(command)


# 重启adb server
def reboot_adb():
    device_id_list = ["192.168.31.123:5555"]
    command = "adb kill-server"
    opt_sys_command(command)
    command = "adb start-server"
    opt_sys_command(command)
    for i in device_id_list:
        command = "adb connect " + i
        opt_sys_command(command)
    # 获取连接的device_list
    connected_device_id_list = get_all_device_id()
    no_device_id_list = set(device_id_list) - set(connected_device_id_list)
    print(
        "已连接%s设备：%s" % (len(connected_device_id_list), " ".join(connected_device_id_list))
    )
    print(
        "未连接%s设备：%s" % (len(no_device_id_list), " ".join(no_device_id_list))
    )

def get_random_time():
    # 随机生产事件间隔
    return random.randint(3, 9)

def main():
    device_id_list = get_all_device_id()
    for device_id in device_id_list:
        up_short_swipe(device_id)


if __name__ == "__main__":
    main()
