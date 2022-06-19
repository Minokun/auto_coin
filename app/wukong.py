# -*- coding:utf-8 -*-
import math, re
import time

from utils.phone_opt import *


# 今日头条极速版
class WuKongOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "wk_browser"
        self.app_name_chinese = app_name[self.app_name]
        self.current_step = ''
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        # 底部我的金币按钮
        self.coin_button = (540, int(2340 * self.height_scale))
        # 猴子金币按钮
        self.monkey_button = ()
        # 当前金币和现金收益
        self.coin_current = 0.0
        self.cash_current = 0.0
        self.coin_today = 0.0
        self.cash_total = 0.0

    def start_wk_app(self):
        print_help_text(self.device_id, "启动悟空浏览器")
        # 启动悟空浏览器
        start_app(self.device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)
        status, position = find_screen_text_button_position(self.device_id, "我知道", "我知道")
        if status:
            tap(self.device_id, position)
        status, position = find_screen_text_button_position(self.device_id, "看广告", "看广告")
        if status:
            print_help_text(self.device_id, "看广告")
            tap(self.device_id, position)
            self.watch_ad()


    # 上滑到最顶部
    def back_top(self):
        for i in range(4):
            down_long_swipe(self.device_id)

    def get_coin_num(self):
        print_help_text(self.device_id, "获取当前收益")
        self.back_to_main()
        # 点击任务
        tap(self.device_id, self.coin_button)
        time.sleep(1)
        self.back_top()
        coin = self.coin_current
        cash = self.cash_current
        stats, box, result = find_screen_text_position(self.device_id, "金币")
        for line in result:
            if line[1][0].find('.') >= 0:
                g = re.findall(r'[^\d]*([\d]+\.[\d]+)元*', line[1][0])
                if len(g) > 0:
                    cash = float(g[0])
            g = re.findall(r'[^\d]*([\d]+)[^\d]*金币', line[1][0])
            if len(g) > 0:
                coin = float(g[0])
                break
        print_help_text(self.device_id, "当前金币：%s 当前现金：%s" % (str(coin), str(cash)))
        return coin, cash

    def shut_app(self):
        shut_app(self.device_id, self.app_name)

    def back_to_main(self):
        for i in range(6):
            print_help_text(self.device_id, "回到首页")
            status, position = find_screen_text_button_position(self.device_id, "首页", "首页", top_normal_bottom='bottom')
            # 如果有就退出
            if status:
                tap(self.device_id, position)
                break
            else:
                press_back(self.device_id)
            time.sleep(1)
            if i > 4:
                self.shut_app()
                time.sleep(1)
                self.start_wk_app()
                break

    def watch_video(self):
        pass

    def watch_xiaoshuo(self):
        pass

    # 看广告
    def watch_ad(self):
        status = False
        while not status:
            stats, position = find_screen_text_button_position(self.device_id, "首页", "首页", top_normal_bottom="bottom")
            if stats:
                print_help_text("回到了首页")
                return True
            stats, box, result = find_screen_text_position(self.device_id, "看视频再领")
            if stats:
                print_help_text(self.device_id, "看视频广告领金币")
                position = find_screen_by_result(result, "看视频再领")
                tap(self.device_id, position)
            position = find_screen_by_result(result, "再看一")
            if position:
                print_help_text(self.device_id, "再看一个视频")
                tap(self.device_id, position)
            position = find_screen_by_result(result, "继续观看")
            if position:
                print_help_text(self.device_id, "继续观看")
                tap(self.device_id, position)
            time.sleep(15)
            press_back(self.device_id)

    def auto_coin_box(self):
        # 看宝箱的广告
        print_help_text(self.device_id, "点击任务菜单，开始看宝箱广告")
        # 点击任务菜单
        self.back_to_main()
        tap(self.device_id, self.coin_button)
        # 返会再点击一次 为了防止布局不一样
        up_long_swipe(self.device_id)
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            print_help_text(self.device_id, "开宝箱")
            # 点击宝箱
            tap(self.device_id, position)
            time.sleep(1)
            # 点击”看视频再领“ 开始看广告
            tap(self.device_id, self.ads_position)
            # 循环查看
            self.watch_ad()
        else:
            print_help_text(self.device_id, "目前不能点击宝箱！")

    # 看广告
    def auto_watch_ad(self):
        # 点击任务菜单
        self.back_to_main()
        print_help_text(self.device_id, "点击任务菜单,开始看广告")
        tap(self.device_id, self.coin_button)
        # 上滑找“看广告” 最多5次
        for i in range(3):
            # 上滑
            up_long_swipe(self.device_id)
            status, position = find_screen_text_button_position(self.device_id, "看广告视频", "去完成")
            if status:
                print_help_text(self.device_id, "看广告")
                tap(self.device_id, position)
                self.watch_ad()
                return True
        print_help_text(self.device_id, "未找到看广告领福利的位置！")

    # TODO 自动领取所有奖励
    def auto_take_award(self):
        self.back_to_main()
        # 点击我的金币页面
        tap(self.device_id, self.coin_button)
        # 点击猴子领金币
        stats, position = find_screen_text_button_position(self.device_id, "领取金币", "领取金币")
        if stats:
            print_help_text(self.device_id, "点击领取金币")
            tap(self.device_id, position)
            self.watch_ad()
        while True:
            stats, position = find_screen_text_button_position(self.device_id, "看视频", "看视频")
            if stats:
                print_help_text(self.device_id, "看广告")
                tap(self.device_id, position)
                self.watch_ad()
            else:
                break


    # 开始自动刷app
    def auto_run(self, light_screen_stats=True):
        # 解锁屏幕
        if light_screen_stats:
            print_help_text(self.device_id, "解锁设备")
            unlock_device(self.device_id)
        # 启动app
        self.start_wk_app()
        time.sleep(1)
        # 获取当前收益
        coin_start, cash_start = self.get_coin_num()
        #
        # 获取当前收益
        coin_end, cash_end = self.get_coin_num()
        self.coin_current = coin_end - coin_start
        self.cash_current = round(self.coin_current / 33000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end


if __name__ == "__main__":
    article_obj = WuKongOpt("192.168.101.101:5555")

    article_obj.auto_run(light_screen_stats=False)