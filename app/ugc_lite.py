# -*- coding:utf-8 -*-

import math
import time
from config import TIMES
from utils.phone_opt import *


# 抖音极速版
class UGCLiteOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        self.app_name = "ugc_lite"
        self.app_name_chinese = app_name[self.app_name]
        self.current_step = ''
        # 首页底部任务按钮
        self.main_coin_position = (550, int(2330 * self.height_scale))
        # 关闭广告的按键
        self.ad_shut = (990, int(150 * self.height_scale))
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, int(1380 * self.height_scale))
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, int(1370 * self.height_scale))
        self.coin_box_ad_shut = (530, int(1660 * self.height_scale))
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
        time.sleep(1)
        stats, box, result = find_screen_text_position(self.device_id, "我知道")
        position = find_screen_by_result(result, "拒绝")
        if position:
            tap(self.device_id, position)
        position = find_screen_by_result(result, "我知道")
        if position:
            tap(self.device_id, position)
        position = find_screen_by_result(result, "继续观看")
        if position:
            tap(self.device_id, position)

    def shut_app(self):
        shut_app(self.device_id, self.app_name)

    def get_coin_num(self):
        print_help_text(self.device_id, "获取收益")
        # 获取当前金币数量
        self.back_main_coin()
        time.sleep(2)
        status, position = find_screen_text_button_position(self.device_id, "立即签到", "立即签到")
        if status:
            tap(self.device_id, position)
            time.sleep(1)
            tap(self.device_id, position)
            self.ad()
        self.back_top()
        stats, box, result = find_screen_text_position(self.device_id, "现金收益")
        if not stats:
            coin, cash = self.get_coin_num()
            return coin, cash
        y_bottom = box[2][1] + 5
        n = 0
        coin = 0.0
        cash = 0.0
        for line in result:
            if line[0][2][1] > y_bottom:
                n += 1
                if n == 1:
                    try:
                        coin = float(line[1][0])
                    except Exception as e:
                        print(self.device_id, e)
                        coin = 0.0
                elif n == 2:
                    try:
                        cash = float(line[1][0])
                    except Exception as e:
                        print(self.device_id, e)
                        cash = 0.0
                else:
                    break
        print_help_text(self.device_id, "当前金币：%s 当前现金：%s" % (str(coin), str(cash)))
        return coin, cash

    # 看视频
    def watch_video(self):
        self.back_main_coin()
        # 点击返回
        press_back(self.device_id)
        if self.device_id in TIMES[self.app_name]['watch_video_numbers'].keys():
            num = TIMES[self.app_name]['watch_video_numbers'][self.device_id]
        else:
            num = TIMES[self.app_name]['watch_video_numbers']['default']
        for i in range(num):
            print_help_text(self.device_id, "第%s/%s次刷视频" % (str(i + 1), str(num)))
            up_short_swipe(self.device_id)
            time.sleep(get_random_time(5, 10))

    # 返回首页再进入任务页面
    def back_main_coin(self):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            print_help_text(self.device_id, "回到首页")
            status, _, _ = find_screen_text_position(self.device_id, "推荐", top_normal_bottom='top')
            # 如果在首页就点击，没有就返回
            if status:
                print_help_text(self.device_id, "进入金币页面")
                tap(self.device_id, self.main_coin_position)
                # stats, position = find_screen_text_button_position(self.device_id, "看广告视频再赚", "看广告视频再赚")
                # if stats:
                #     tap(self.device_id, position)
                #     self.ad()
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
        for i in range(5):
            down_long_swipe(self.device_id)

    # 看广告
    def ad(self):
        while True:
            print_help_text(self.device_id, "看广告")
            # 点击看广告
            time.sleep(30)
            ad_status, position = find_screen_text_button_position(self.device_id, "反馈", "反馈")
            if ad_status:
                print_help_text(self.device_id, "关闭广告")
                tap(self.device_id, self.ad_shut)
            else:
                stats, _ = find_screen_text_button_position(self.device_id, "X", "X")
                if not stats:
                    press_back(self.device_id)
                print_help_text(self.device_id, "关掉当前广告页再点击关掉广告")
                tap(self.device_id, (60, 150))
                time.sleep(1)
                tap(self.device_id, self.ad_shut)
                # stats, position = find_screen_text_button_position(self.device_id, "广告", '广告', top_normal_bottom='top')
                # if stats:
                #     press_back(self.device_id)
                #     break
            time.sleep(1)
            status, lq_position = find_screen_text_button_position(self.device_id, "领取奖励", "领取奖励")
            if lq_position:
                print_help_text(self.device_id, "领取奖励")
                tap(self.device_id, lq_position)
                continue
            else:
                ad_status, position = find_screen_text_button_position(self.device_id, "反馈", "反馈")
                if ad_status:
                    print_help_text(self.device_id, "再次关闭广告")
                    tap(self.device_id, self.ad_shut)

            status, jx_position = find_screen_text_button_position(self.device_id, "继续", "继续")
            if status:
                print_help_text(self.device_id, "继续观看")
                tap(self.device_id, jx_position)
                time.sleep(10)
                print_help_text(self.device_id, "关掉广告")
                tap(self.device_id, self.ad_shut)
            break

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
        print_help_text(self.device_id, "完成看广告")

    # 刷宝箱
    def coin_box(self):
        # 刷宝箱
        self.back_main_coin()
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            tap(self.device_id, position)
            time.sleep(1)
            # 点击看广告
            stats, box, result = find_screen_text_position(self.device_id, "频再赚")
            if stats:
                position = find_screen_by_result(result, "频再赚")
                tap(self.device_id, (position[0] - 10, position[1] + 10))
                self.ad()
            position = find_screen_by_result(result, "立赚高额")
            if position:
                tap(self.device_id, self.coin_box_ad_shut)
        else:
            print_help_text(self.device_id, "当前无宝箱可看")

    # 刷爆款
    def watch_baokuan(self):
        # 进入金币页面
        self.back_main_coin()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找浏览爆款的按钮")
            status, position = find_screen_text_button_position(self.device_id, "爆款", "赚")
            if status:
                tap(self.device_id, position)
                break
            up_long_swipe(self.device_id)
        if not status:
            return False
        time.sleep(1)
        print_help_text(self.device_id, "开始刷爆款1分钟")
        status, position = find_screen_text_button_position(self.device_id, "点击领取", "点击领取")
        if status:
            print_help_text(self.device_id, "点击领取金币")
            tap(self.device_id, position)
        for i in range(75):
            print_help_text(self.device_id, "第%s/75次" % str(i + 1))
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
            else:
                stats, position = find_screen_text_button_position(self.device_id, "逛", "赚金币")
                if position:
                    button_position = position
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
        print_help_text(self.device_id, "今天逛街奖励已经领取完毕！")

    def auto_run(self, first_status=False, light_screen_stats=True, watch_video=True, watch_baokuan=True, search=True, watch_coin_box=True,
                 watch_ad=True, walk=True, shopping=True):
        # 解锁手机
        if light_screen_stats:
            print_help_text(self.device_id, "解锁手机")
            unlock_device(self.device_id)
        # 打开抖音极速版
        print_help_text(self.device_id, "打开抖音极速版")
        self.start_ugc_app()
        time.sleep(1)
        # 获取当前金币和现金收益
        coin_start, cash_start = self.get_coin_num()
        # 看10分钟视频
        if watch_video:
            self.current_step = self.app_name_chinese + '(看10分钟视频)'
            print_help_text(self.device_id, "开始看视频", self.current_step)
            self.watch_video()
        # 看爆款
        if watch_baokuan:
            self.current_step = self.app_name_chinese + '(看爆款)'
            print_help_text(self.device_id, "开始刷爆款", self.current_step)
            self.watch_baokuan()
        # 看广告
        if watch_ad:
            self.current_step = self.app_name_chinese + '(看广告)'
            print_help_text(self.device_id, "开始看广告", self.current_step)
            self.watch_ad()
        # 看宝箱
        if watch_coin_box:
            self.current_step = self.app_name_chinese + '(开宝箱)'
            print_help_text(self.device_id, "刷宝箱", self.current_step)
            self.coin_box()
        # 逛街
        if shopping:
            self.current_step = self.app_name_chinese + '(逛街)'
            print_help_text(self.device_id, "逛街", self.current_step)
            self.shopping()
        time.sleep(5)
        # 再次获取当前金币和现金收益
        coin_end, cash_end = self.get_coin_num()
        self.coin_current = coin_end - coin_start
        self.cash_current = round(self.coin_current / 10000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end


if __name__ == "__main__":
    ugc_lite_obj = UGCLiteOpt("192.168.101.104:5555")
    ugc_lite_obj.auto_run(light_screen_stats=False, watch_video=False, watch_baokuan=False, watch_ad=False,
                          watch_coin_box=True)
    print(ugc_lite_obj.get_coin_num())
    # device_id = '192.168.31.228:5555'
    # position = (520, 1318)
    # for i in range(4):
    #     tap(device_id, position)
