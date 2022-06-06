# -*- coding:utf-8 -*-

import math
import time

from phone_opt import *


# 抖音极速版
class KuaiShouOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "kuaishou"
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        # 首页
        self.main_position = (100, int(2330 * self.height_scale))
        # 去赚钱
        self.task_position = (780, int(2300 * self.height_scale))
        # 关闭广告的按键
        self.ad_shut = (980, int(150 * self.height_scale))
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, int(1380 * self.height_scale))
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, int(1450 * self.height_scale))

    def start_huaishou_app(self):
        start_app(self.device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            time.sleep(0.5)
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)

    # 看视频
    def watch_video(self, times=30):
        self.back_main_coin()
        tap(self.device_id, self.main_position)
        for i in range(times):
            print_help_text(self.device_id, "第%s/%s次刷视频" % (str(i + 1), str(times)))
            up_short_swipe(self.device_id)
            time.sleep(get_random_time(10, 15))

    # 返回首页再进入任务页面
    def back_main_coin(self):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            print_help_text(self.device_id, "回到首页")
            stats, positon = find_screen_text_button_position(self.device_id, "首页", "首页", top_normal_bottom="bottom")
            if stats:
                break
            else:
                press_back(self.device_id)
            if i > 5:
                self.start_huaishou_app()

    # 上滑到最顶部
    def back_top(self):
        for i in range(3):
            down_long_swipe(self.device_id)

    # 看广告
    def ad(self):
        while True:
            print_help_text(self.device_id, "开始看广告")
            time.sleep(27)
            tap(self.device_id, (280, 200))
            stats, position = find_screen_text_button_position(self.device_id, "去完成", "去完成")
            if stats:
                tap(self.device_id, position)
                time.sleep(1)
                tap(self.device_id, (280, 200))
            stats, position = find_screen_text_button_position(self.device_id, "再看一个", "再看一个")
            if stats:
                print_help_text(self.device_id, "再看一个")
                tap(self.device_id, position)
                continue
            break

    # 刷广告
    def watch_ad(self):
        # 先回到首页
        self.back_main_coin()
        # 点击去赚钱
        tap(self.device_id, self.task_position)
        self.back_top()
        self.rm_ad()
        for i in range(3):
            print_help_text(self.device_id, "找看广告按钮")
            stats, position = find_screen_text_button_position(self.device_id, "金币悬赏", "福利")
            if stats:
                print_help_text(self.device_id, "点击看广告")
                tap(self.device_id, position)
                self.ad()
                break
            else:
                up_long_swipe(self.device_id)

    # 关掉广告
    def rm_ad(self):
        time.sleep(1)
        stats, box, result = find_screen_text_position(self.device_id, "看视频最高得")
        # TODO
        if stats:
            # 点击查看视频
            print_help_text(self.device_id, "直接点击看广告")
            position = find_screen_by_result(result, "看视频最高")
            tap(self.device_id, position)
            self.ad()
            return True
        position = find_screen_by_result(result, "X")
        if position:
            tap(self.device_id, position)

    # 刷宝箱
    def coin_box(self):
        # 刷宝箱
        self.back_main_coin()
        tap(self.device_id, self.task_position)
        self.rm_ad()
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            print_help_text(self.device_id, "开宝箱")
            tap(self.device_id, position)
            time.sleep(1)
            # 点击看广告
            tap(self.device_id, self.coin_box_ad)
            self.ad()
        else:
            print_help_text(self.device_id, "当前无宝箱可看")

    def shopping(self):
        self.back_main_coin()
        # 点击红包菜单
        print_help_text(self.device_id, "点击去赚钱")
        tap(self.device_id, self.task_position)
        self.rm_ad()
        for i in range(4):
            stats, position = find_screen_text_button_position(self.device_id, "逛街领", "去逛街")
            if not stats:
                up_long_swipe(self.device_id)
                continue
            else:
                print_help_text(self.device_id, "点击去逛街")
                tap(self.device_id, position)
                for i in range(200):
                    print_help_text(self.device_id, "逛街第%s/200次" % str(i + 1))
                    up_short_swipe(self.device_id)
                    time.sleep(5)
                print_help_text(self.device_id, "返回")
                press_back(self.device_id)
                stats, position = find_screen_text_button_position(self.device_id, "放弃奖励", "放弃奖励")
                if stats:
                    tap(self.device_id, position)

    def auto_run(self, light_screen_stats=False, watch_video=True, watch_coin_box=True, watch_ad=True, shopping=False):
        # 解锁手机
        if light_screen_stats:
            print_help_text(self.device_id, "解锁手机")
            unlock_device(self.device_id)
        # 打开抖音极速版
        print_help_text(self.device_id, "打开快手")
        self.start_huaishou_app()
        time.sleep(1)
        # 看广告
        if watch_ad:
            self.watch_ad()
        # 看宝箱
        if watch_coin_box:
            print_help_text(self.device_id, "刷宝箱")
            self.coin_box()
        # 看10分钟视频
        if watch_video:
            print_help_text(self.device_id, "开始看视频")
            self.watch_video()
        # 逛街
        if shopping:
            print_help_text(self.device_id, "去逛街")
            self.shopping()


if __name__ == "__main__":
    ks_obj = KuaiShouOpt("192.168.101.103:5555")
    ks_obj.auto_run(light_screen_stats=False, watch_video=True, watch_ad=True, watch_coin_box=True, shopping=True)
