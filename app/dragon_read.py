# -*- coding:utf-8 -*-
import time

from utils.phone_opt import *
import re

# 抖音极速版
class DragonReadOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "dragon_read"
        self.app_name_chinese = app_name[self.app_name]
        self.current_step = ''
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        # 首页底部任务按钮
        self.main_coin_position = (550, int(2330 * self.height_scale))
        # 关闭广告的按键
        self.ad_shut = (980, int(160 * self.height_scale))
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, int(1380 * self.height_scale))
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, int(1450 * self.height_scale))
        # 当前金币和现金收益
        self.coin_current = 0.0
        self.cash_current = 0.0
        self.coin_today = 0.0
        self.cash_total = 0.0

    def start_dragon_app(self):
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
        time.sleep(3)
        stats, box, result = find_screen_text_position(self.device_id, "立即签到")
        if stats:
            print_help_text(self.device_id, "签到")
            position = find_screen_by_result(result, "立即签到")
            tap(self.device_id, position)
            time.sleep(0.5)
            tap(self.device_id, position)
            self.ad()
        self.back_top()
        stats, box, result = find_screen_text_position(self.device_id, "金币收益")
        if not stats:
            return self.get_coin_num()
        coin = self.coin_current
        cash = self.cash_current
        for line in result:
            if line[0][0][1] > box[0][1]:
                if line[1][0].find('.') >= 0:
                    g = re.findall(r'[^\d]*([\d]+\.[\d]+)元*', line[1][0])
                    if len(g) > 0:
                        cash = float(g[0])
                g = re.findall(r'^([\d]+)[币]*$', line[1][0])
                if len(g) > 0:
                    coin = float(g[0])
                    break
        print_help_text(self.device_id, "当前金币：%s 当前现金：%s" % (str(coin), str(cash)))
        return coin, cash

    # 返回首页再进入任务页面
    def back_main_coin(self):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            # print_help_text(self.device_id, "回到首页")
            status, _, _ = find_screen_text_position(self.device_id, "书架", top_normal_bottom='bottom')
            # 如果在首页就点击，没有就返回
            if status:
                print_help_text(self.device_id, "进入金币页面")
                tap(self.device_id, self.main_coin_position)
                time.sleep(1.5)
                stats, position = find_screen_text_button_position(self.device_id, "立即签到", '立即签到')
                if stats:
                    tap(self.device_id, position)
                    self.ad()
                break
            else:
                press_back(self.device_id)
            if i > 4:
                self.shut_app()
                time.sleep(1)
                self.start_dragon_app()
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
            time.sleep(30)
            status_continue, box, result = find_screen_text_position(self.device_id, "再看")
            main_position = find_screen_by_result(result, "书架")
            if main_position:
                print_help_text(self.device_id, "回到了首页")
                break
            position = find_screen_by_result(result, "再看")
            if status_continue:
                print_help_text(self.device_id, "继续")
                tap(self.device_id, position)
                continue
            jump_position = find_screen_by_result(result, "跳过")
            if jump_position:
                continue
            time.sleep(1)
            tap(self.device_id, self.ad_shut)
            status = False

    # 刷广告
    def watch_ad(self):
        # 进入金币页面
        self.back_main_coin()
        self.back_top()
        for i in range(4):
            print_help_text(self.device_id, "找看广告的按钮")
            status, box, result = find_screen_text_position(self.device_id, "立即观看")
            position_1 = find_screen_by_result(result, "立即观看")
            position_2 = find_screen_by_result(result, "去观看")
            position = position_1 if position_1 else position_2
            if position:
                tap(self.device_id, position)
                time.sleep(0.5)
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
        # 获取当前收益
        coin_start, cash_start = self.get_coin_num()
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
        self.cash_current = round(self.coin_current / 33000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end

if __name__ == "__main__":
    # print(dragon_read_obj.get_coin_num())
    for i in range(50):
        dragon_read_obj = DragonReadOpt("192.168.101.104:5555")
        dragon_read_obj.auto_run(light_screen_stats=False)
