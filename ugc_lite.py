# -*- coding:utf-8 -*-

import math

from phone_opt import *


# 抖音极速版
class UGCLiteOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "ugc_lite"
        # 首页底部任务按钮
        self.main_coin_position = (550, 2330)
        # 关闭广告的按键
        self.ad_shut = (980, 150)
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, 1380)
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, 1450)

    def start_ugc_app(self):
        start_app(self.device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)

    # 看视频
    def watch_video(self, time_period=600000):
        self.back_main_coin()
        # 点击返回
        press_back(self.device_id)
        per_video_time = 6000
        num = math.ceil(time_period / per_video_time)
        for i in range(num):
            print_help_text(self.device_id, "第%s/%s次刷视频" % (str(i + 1), str(num)))
            up_short_swipe(self.device_id)
            time.sleep(get_random_time(5, 10))

    # 返回首页再进入任务页面
    def back_main_coin(self):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            print_help_text(self.device_id, "回到首页")
            status, _, _ = find_screen_text_position(self.device_id, "首页")
            # 如果在首页就点击，没有就返回
            if status:
                print_help_text(self.device_id, "进入金币页面")
                tap(self.device_id, self.main_coin_position)
                break
            else:
                press_back(self.device_id)
                stats, position = find_screen_text_button_position(self.device_id, "坚持退出", "坚持退出")
                if stats:
                    tap(self.device_id, position)

    # 上滑到最顶部
    def back_top(self):
        for i in range(4):
            down_long_swipe(self.device_id)

    # 看广告
    def ad(self):
        status = True
        while status:
            print_help_text(self.device_id, "看广告")
            time.sleep(34)
            for i in range(3):
                ad_status, position = find_screen_text_button_position(self.device_id, "X", "X")
                if ad_status:
                    print_help_text(self.device_id, "关闭广告")
                    tap(self.device_id, position)
                    break
                else:
                    press_back(self.device_id)
            time.sleep(2)
            status, _, _ = find_screen_text_position(self.device_id, "再看")
            if status:
                tap(self.device_id, self.ad_continue_menu_position)

    # 刷广告
    def watch_ad(self):
        # 进入金币页面
        self.back_main_coin()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找看广告的按钮")
            status, position = find_screen_text_button_position(self.device_id, "看广告", "去领取")
            if status:
                tap(self.device_id, position)
                self.ad()
                break
            up_long_swipe(self.device_id)
        print_help_text(self.device_id, "当前无广告可看")

    # 刷宝箱
    def coin_box(self):
        # 刷宝箱
        self.back_main_coin()
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            tap(self.device_id, position)
            time.sleep(0.5)
            # 点击看广告
            tap(self.device_id, self.coin_box_ad)
            self.ad()
        else:
            print_help_text(self.device_id, "当前无宝箱可看")

    # 刷爆款
    def watch_baokuan(self):
        # 进入金币页面
        self.back_main_coin()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找浏览爆款的按钮")
            status, position = find_screen_text_button_position(self.device_id, "浏览爆款", "赚金币")
            if status:
                tap(self.device_id, position)
                break
            up_long_swipe(self.device_id)
        print_help_text(self.device_id, "开始刷爆款1分钟")
        status, position = find_screen_text_button_position(self.device_id, "点击领取", "点击领取")
        if status:
            print_help_text(self.device_id, "点击领取金币")
            tap(self.device_id, position)
        for i in range(70):
            print_help_text(self.device_id, "第%s/70次" % str(i + 1))
            up_short_swipe(self.device_id)
        print_help_text(self.device_id, "返回")
        press_back(self.device_id)

    # 逛街赚钱
    def shopping(self):
        self.back_main_coin()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找逛街的按钮")
            status, box, result = find_screen_text_position(self.device_id, "去逛街")
            button_position = find_screen_by_result(result, "去逛街")
            if button_position:
                break
            up_long_swipe(self.device_id)
        if not button_position:
            print_help_text(self.device_id, "没有找到逛街按钮")
            return True
        # 如果未逛满15次 开始逛街
        position = find_screen_by_result(result, "10/10")
        if not position:
            tap(self.device_id, button_position)
            print_help_text(self.device_id, "开始逛街2分钟")
            time.sleep(2)
            for i in range(13):
                print_help_text(self.device_id, "第%s/13次" % str(i + 1))
                time.sleep(get_random_time(8, 12))
                up_short_swipe(self.device_id)
            print_help_text(self.device_id, "返回")
            press_back(self.device_id)
            # 如果没逛完 直接退出
            stats, position = find_screen_text_button_position(self.device_id, "坚持退出", "坚持退出")
            if stats:
                tap(self.device_id, position)
        print("今天逛街奖励已经领取完毕！")

    def auto_run(self, light_screen_stats=True, watch_video=True, watch_baokuan=True, search=True, watch_coin_box=True,
                 watch_ad=True, walk=True, shopping=True):
        # 解锁手机
        if light_screen_stats:
            print_help_text(self.device_id, "解锁手机")
            unlock_device(self.device_id)
        # 打开抖音极速版
        print_help_text(self.device_id, "打开抖音极速版")
        self.start_ugc_app()
        time.sleep(1)
        # 看10分钟视频
        if watch_video:
            print_help_text(self.device_id, "开始看视频")
            self.watch_video()
        # 看爆款
        if watch_baokuan:
            print_help_text(self.device_id, "开始刷爆款")
            self.watch_baokuan()
        # 看广告
        if watch_ad:
            print_help_text(self.device_id, "开始看广告")
            self.watch_ad()
        # 看宝箱
        if watch_coin_box:
            print_help_text(self.device_id, "刷宝箱")
            self.coin_box()
        # 逛街
        if shopping:
            print_help_text(self.device_id, "逛街")
            self.shopping()
        time.sleep(5)


if __name__ == "__main__":
    ugc_lite_obj = UGCLiteOpt("192.168.101.103:5555")
    ugc_lite_obj.auto_run(light_screen_stats=False, watch_video=False, watch_baokuan=False, watch_ad=False,
                          watch_coin_box=False)
