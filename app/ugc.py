# -*- coding:utf-8 -*-

import math

from utils.phone_opt import *


# 抖音极速版
class UGCOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "ugc"
        self.app_name_chinese = app_name[self.app_name]
        self.current_step = ''
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        # 首页底部任务按钮
        self.my_position = (970, int(2320 * self.height_scale))
        self.my_task_position = (980, int(190 * self.height_scale))
        self.main_position = (100, int(2330 * self.height_scale))
        # 关闭广告的按键
        self.ad_shut = (980, int(150 * self.height_scale))
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, int(1380 * self.height_scale))
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, int(1450 * self.height_scale))
        # 当前金币和现金收益
        self.coin_current = 0.0
        self.cash_current = 0.0
        self.coin_today = 0.0
        self.cash_total = 0.0

    def start_ugc_app(self):
        start_app(self.device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)

    def shut_app(self):
        shut_app(self.device_id, self.app_name)

    def get_coin_num(self):
        self.back_main_coin()
        self.back_top()
        stats, box, result = find_screen_text_position(self.device_id, "金币收益")
        if not stats:
            return self.coin_current, self.cash_current
        y_bottom = box[2][1]
        coin = 0.0
        for line in result:
            if line[0][2][1] > y_bottom:
                coin = float(line[1][0].replace(',', '.'))
                coin = coin if coin - round(coin, 0) == 0 else coin * 1000
                break
        cash = round(coin / 10000, 2)
        print_help_text(self.device_id, "当前金币：%s 当前现金：%s" % (str(coin), str(cash)))
        return coin, cash

    # 看视频
    def watch_video(self, time_period=60000):
        for i in range(4):
            print_help_text(self.device_id, "回到首页")
            main_status, _, result = find_screen_text_position(self.device_id, "首页", top_normal_bottom='bottom')
            if main_status:
                break
            else:
                press_back(self.device_id)
        # 点击首页
        tap(self.device_id, self.main_position)
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
            main_status, _, result = find_screen_text_position(self.device_id, "首页", top_normal_bottom='bottom')
            # 如果在首页就点击，没有就返回
            if main_status:
                print_help_text(self.device_id, "点击右下角的我")
                tap(self.device_id, self.my_position)
                print_help_text(self.device_id, "点击右上角任务")
                tap(self.device_id, self.my_task_position)
                print_help_text(self.device_id, "点击钱包")
                stats, position = find_screen_text_button_position(self.device_id, "钱包", "钱包")
                if stats:
                    tap(self.device_id, position)
                else:
                    break
                up_short_swipe(self.device_id)
                print_help_text(self.device_id, "点击赚金币")
                stats, position = find_screen_text_button_position(self.device_id, "赚金币", "赚金币")
                if stats:
                    tap(self.device_id, position)
                break
            else:
                press_back(self.device_id)
                stats, position = find_screen_text_button_position(self.device_id, "坚持退出", "坚持退出")
                if stats:
                    tap(self.device_id, position)
            if i > 4:
                self.shut_app()
                time.sleep(1)
                self.start_ugc_app()
                break

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
            stats, box, result = find_screen_text_position(self.device_id, "开心收下")
            if stats:
                # 结束看广告
                print_help_text(self.device_id, "开心收下")
                position = find_screen_by_result(result, "开心收下")
                tap(self.device_id, position)
                break
            position = find_screen_by_result(result, "再看")
            if position:
                print_help_text(self.device_id, "继续看广告")
                tap(self.device_id, position)
                continue
            position = find_screen_by_result(result, "活动时间")
            if position:
                status = False
            print_help_text(self.device_id, "点击关闭广告")
            tap(self.device_id, self.ad_shut)
            break
        stats, position = find_screen_text_button_position(self.device_id, "开心收下", "开心收下")
        if stats:
            tap(self.device_id, position)



    # 刷广告
    def watch_ad(self):
        # 进入金币页面
        self.back_main_coin()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找看广告的按钮")
            status, position = find_screen_text_button_position(self.device_id, "看广告视频", "去看看")
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
        up_long_swipe(self.device_id)
        status, position = find_screen_text_button_position(self.device_id, "开宝箱领奖", "开宝箱领奖")
        if status:
            print_help_text(self.device_id, "开宝箱")
            tap(self.device_id, position)
            time.sleep(0.5)
            # 点击看广告
            tap(self.device_id, self.coin_box_ad)
            self.ad()
        else:
            print_help_text(self.device_id, "当前无宝箱可看")


    def auto_run(self, light_screen_stats=True, watch_video=True, watch_coin_box=True, watch_ad=True):
        # 解锁手机
        if light_screen_stats:
            print_help_text(self.device_id, "解锁手机")
            unlock_device(self.device_id)
        # 打开抖音极速版
        print_help_text(self.device_id, "打开抖音")
        self.start_ugc_app()
        time.sleep(1)
        # 获取当前收益
        coin_start, cash_start = self.get_coin_num()
        # 看10分钟视频
        if watch_video:
            print_help_text(self.device_id, "开始看视频")
            self.watch_video()
        # 看广告
        if watch_ad:
            print_help_text(self.device_id, "开始看广告")
            self.watch_ad()
        # 看宝箱
        if watch_coin_box:
            print_help_text(self.device_id, "刷宝箱")
            self.coin_box()
        # 获取当前收益
        coin_end, cash_end = self.get_coin_num()
        self.coin_current = coin_end - coin_start
        self.cash_current = round(self.coin_current / 10000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end


if __name__ == "__main__":
    ugc_obj = UGCOpt("192.168.31.212:5555")
    ugc_obj.auto_run(light_screen_stats=False, watch_video=False, watch_ad=True, watch_coin_box=True)
