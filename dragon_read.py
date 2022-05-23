# -*- coding:utf-8 -*-

import math
import time

from phone_opt import *


# 抖音极速版
class DragonReadOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "dragon_read"
        # 首页底部任务按钮
        self.main_coin_position = (550, 2330)
        # 关闭广告的按键
        self.ad_shut = (980, 160)
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, 1380)
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, 1450)

    def start_dragon_app(self):
        start_app(self.device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)

    # 返回首页再进入任务页面
    def back_main_coin(self):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            print_help_text(self.device_id, "回到首页")
            status, _, _ = find_screen_text_position(self.device_id, "书架")
            # 如果在首页就点击，没有就返回
            if status:
                print_help_text(self.device_id, "进入金币页面")
                tap(self.device_id, self.main_coin_position)
                break
            else:
                press_back(self.device_id)

    # 上滑到最顶部
    def back_top(self):
        for i in range(4):
            down_long_swipe(self.device_id)

    # 看广告
    def ad(self):
        status = True
        while status:
            print_help_text(self.device_id, "看广告")
            time.sleep(17)
            status_continue, box, result = find_screen_text_position(self.device_id, "再看")
            main_position = find_screen_by_result(result, "书架")
            if main_position:
                print_help_text(self.device_id, "回到了首页")
                break
            position = find_screen_by_result(result, "再看")
            if status_continue:
                print_help_text(self.device_id, "继续下一个广告")
                tap(self.device_id, position)
                continue
            jump_position = find_screen_by_result(result, "跳过")
            if jump_position:
                continue
            tap(self.device_id, self.ad_shut)

    # 刷广告
    def watch_ad(self):
        # 进入金币页面
        self.back_main_coin()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找看广告的按钮")
            status, position = find_screen_text_button_position(self.device_id, "立即观看", "立即观看")
            if status:
                tap(self.device_id, position)
                self.ad()
                break
            up_long_swipe(self.device_id)

    # 刷宝箱
    def coin_box(self):
        # 刷宝箱
        self.back_main_coin()
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            tap(self.device_id, position)
            time.sleep(0.5)
            #点击看广告
            tap(self.device_id, self.coin_box_ad)
            self.ad()
        else:
            print_help_text(self.device_id, "当前无宝箱可看")

    def jump_main_ad(self):
        # 如果有 跳过广告
        status, position = find_screen_text_button_position(self.device_id, "跳过广告", "跳过广告")
        if status:
            tap(self.device_id, position)

    def auto_run(self, light_screen_stats=True, watch_coin_box=True, watch_ad=True):
        # 解锁手机
        if light_screen_stats:
            print_help_text(self.device_id, "解锁手机")
            unlock_device(self.device_id)
        # 打开番茄小说
        print_help_text(self.device_id, "番茄小说")
        self.start_dragon_app()
        time.sleep(1)
        self.jump_main_ad()
        # 看广告
        if watch_ad:
            print_help_text(self.device_id, "开始看广告")
            self.watch_ad()
        # 看宝箱
        if watch_coin_box:
            print_help_text(self.device_id, "刷宝箱")
            self.coin_box()

if __name__ == "__main__":
    dragon_read_obj = DragonReadOpt("192.168.101.103:5555")
    dragon_read_obj.auto_run(light_screen_stats=False)
