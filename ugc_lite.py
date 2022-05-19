# -*- coding:utf-8 -*-

import math
from phone_opt import *
from paddle_opt import *


# 抖音极速版
class UGCLiteOpt:
    def __init__(self):
        self.device_id_list = get_all_device_id()
        self.paddle_detect = paddle_ocr_obj
        self.app_name = "ugc_lite"
        # 关闭广告的按键
        self.ad_shut = (980, 150)
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, 1380)
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, 1450)

    def start_ugc_app(self, device_id):
        start_app(device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(device_id, "跳过广告", "跳过广告")
            if status:
                tap(device_id, position)

    # 看视频
    def watch_video(self, device_id, time_period=600000):
        per_video_time = 6000
        num = math.ceil(time_period / per_video_time)
        for i in range(num):
            print("第%s/%s次刷视频" % (str(i), str(num)))
            up_short_swipe(device_id)
            time.sleep(get_random_time(5, 10))

    # 返回首页再进入任务页面
    def back_main_coin(self, device_id):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            print("回到首页")
            status, position = find_screen_text_button_position(device_id, "首页", "金币")
            # 如果在首页就点击，没有就返回
            if status:
                print("进入金币页面")
                tap(device_id, position)
                break
            else:
                press_back(device_id)

    # 上滑到最顶部
    def back_top(self, device_id):
        for i in range(4):
            down_long_swipe(device_id)

    # 看广告
    def ad(self, device_id):
        status = True
        while status:
            print("********** 看广告 ************")
            time.sleep(30)
            print("********** 关闭广告 ************")
            tap(device_id, self.ad_shut)
            time.sleep(2)
            status, _, _ = find_screen_text_position(device_id, "再看")
            if status:
                tap(device_id, self.ad_continue_menu_position)

    # 刷广告
    def watch_ad(self, device_id):
        # 进入金币页面
        self.back_main_coin(device_id)
        self.back_top(device_id)
        for i in range(5):
            print("找看广告的按钮")
            status, position = find_screen_text_button_position(device_id, "看广告", "去领取")
            if status:
                tap(device_id, position)
                self.ad(device_id)
                break
            up_long_swipe(device_id)
        print("********** 当前无广告可看 ***********")

    # 刷宝箱
    def coin_box(self, device_id):
        # 刷宝箱
        self.back_main_coin(device_id)
        status, position = find_screen_text_button_position(device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            tap(device_id, position)
            #点击看广告
            tap(device_id, self.coin_box_ad)
            self.ad(device_id)
        else:
            print("******* 当前无宝箱可看 ***************")

    # 刷爆款
    def watch_baokuan(self, device_id):
        # 进入金币页面
        self.back_main_coin(device_id)
        self.back_top(device_id)
        for i in range(5):
            print("********** 找浏览爆款的按钮 ***********")
            status, position = find_screen_text_button_position(device_id, "浏览爆款", "赚金币")
            if status:
                tap(device_id, position)
                break
            up_long_swipe(device_id)
        print("********* 开始刷爆款1分钟 **********")
        status, position = find_screen_text_button_position(device_id, "立即领取", "立即领取")
        if status:
            tap(device_id, position)
        for i in range(60):
            print("第%s/60次" % str(i + 1))
            up_short_swipe(device_id)
        print("******** 返回 ***********")
        press_back(device_id)

    def auto_run(self, light_screen_stats=True, watch_video=True, watch_baokuan=True, search=True, watch_coin_box=True,
                 watch_ad=True, walk=True, eat=True):
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            # 解锁手机
            if light_screen_stats:
                print("*********** 解锁手机 *************")
                unlock_device(device_id)
            # 打开抖音极速版
            print("*********** 打开抖音极速版 ***********")
            self.start_ugc_app(device_id)
            time.sleep(1)
            # 看10分钟视频
            print("*********** 开始看视频 ***********")
            if watch_video:
                self.watch_video(device_id)
            # 看爆款
            print("*********** 开始刷爆款 ***********")
            if watch_baokuan:
                self.watch_baokuan(device_id)
            # 看广告
            print("*********** 开始刷爆款 ***********")
            if watch_ad:
                self.watch_ad(device_id)
            # 看宝箱
            print("*********** 刷宝箱 ***********")
            if watch_coin_box:
                self.coin_box(device_id)


if __name__ == "__main__":
    ugc_lite_obj = UGCLiteOpt()
    ugc_lite_obj.auto_run(watch_video=False, watch_baokuan=False)
