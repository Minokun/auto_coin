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
        # 点击弹出的中间看广告按钮坐标
        self.ads_position = (480, int(1440 * self.height_scale))
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

    # 上滑到最顶部
    def back_top(self):
        for i in range(4):
            down_long_swipe(self.device_id)

    def shut_app(self):
        shut_app(self.device_id, self.app_name)

    def back_to_main(self):
        for i in range(6):
            # print_help_text(self.device_id, "回到首页")
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

    def rm_ad(self):
        print_help_text(self.device_id, "去掉蒙层")
        time.sleep(1)
        stats, position = find_screen_text_button_position(self.device_id, "立即领取", "立即领取")
        if stats:
            tap(self.device_id, position)
            tap(self.device_id, position)
            self.ad()
        stats, position = find_screen_text_button_position(self.device_id, "领取金币", "领取金币")
        if stats:
            print_help_text(self.device_id, "领取金币")
            tap(self.device_id, position)
        while True:
            stats, position = find_screen_text_button_position(self.device_id, "看视频", "看视频")
            if stats:
                print_help_text(self.device_id, "循环点击看视频")
                tap(self.device_id, position)
                time.sleep(0.5)
                tap(self.device_id, self.ads_position)
                self.ad()
            else:
                break
            # 点击任务
            tap(self.device_id, self.coin_button)
            time.sleep(1)

    def get_coin_num(self):
        print_help_text(self.device_id, "获取当前收益")
        self.back_to_main()
        # 点击任务
        tap(self.device_id, self.coin_button)
        time.sleep(2)
        self.back_top()
        # 签到
        stats, position = find_screen_text_button_position(self.device_id, "立即签到", "立即签到")
        if stats:
            print_help_text(self.device_id, "签到")
            tap(self.device_id, position)
            time.sleep(0.5)
            tap(self.device_id, position)
            self.ad()
        self.rm_ad()
        coin = self.coin_current
        cash = self.cash_current
        y_top_limit = 0
        stats, box, result = find_screen_text_position(self.device_id, "我的金币")
        for line in result:
            if line[1][0].find('我的金币') >= 0:
                y_top_limit = line[0][2][1]
                break
        cash_stats = False
        coin_stats = False
        for line in result:
            if line[0][0][1] > y_top_limit:
                if line[1][0].find('.') >= 0:
                    g = re.findall(r'^.*?万.*?([\d]+\.[\d]+)元$', line[1][0])
                    if len(g) > 0:
                        cash = g[0]
                        cash_stats = True

                g = re.findall(r'^([\d]+)$', line[1][0])
                if len(g) > 0:
                    coin = g[0]
                    coin_stats = True
            if cash_stats and coin_stats:
                break
        print_help_text(self.device_id, "当前金币：%s 当前现金：%s" % (str(coin), str(cash)))
        return float(coin), float(cash)

    # 看广告
    def ad(self):
        status = False
        while not status:
            time.sleep(21)
            stats, box, result = find_screen_text_position(self.device_id, "继续观看")
            if stats:
                position = find_screen_by_result(result, '继续观看')
                tap(self.device_id, position)
                time.sleep(6)
            position = find_screen_by_result(result, "再看一")
            if position:
                tap(self.device_id, position)
                continue
            # 如果有查看详情
            stats, box, result = find_screen_text_position(self.device_id, "查看")
            xq_position = find_screen_by_result(result, "查看详情")
            xz_position = find_screen_by_result(result, "立即下载")
            no_pa = find_screen_by_result(result, "平安")
            no_tm = find_screen_by_result(result, "天猫")
            position = xq_position if xq_position else xz_position
            if position and not no_pa and not no_tm:
                print_help_text(self.device_id, "点击查看详情")
                tap(self.device_id, position)
                stats_gg, _ = find_screen_text_button_position(self.device_id, "广告", '广告', top_normal_bottom='top')
                if stats_gg:
                    print_help_text(self.device_id, "刚点击详情没反应，再次点击" + str(position))
                    tap(self.device_id, position)
                for i in range(3):
                    up_long_swipe(self.device_id)
                # 退出详情
                print_help_text(self.device_id, "退出详情")
                tap(self.device_id, (163, 177))
                press_back(self.device_id)
                time.sleep(1)
                # 如果没有回到广告页
                stats, position = find_screen_text_button_position(self.device_id, "广告", '广告', top_normal_bottom="top")
                if not stats:
                    # 再度确认如果有再看 那就再看一个视频
                    zk_stats, zk_position = find_screen_text_button_position(self.device_id, "再看", "再看")
                    if zk_stats:
                        print_help_text(self.device_id, "继续看")
                        tap(self.device_id, zk_position)
                        continue
                    press_back(self.device_id)
                    print_help_text(self.device_id, "跳回到悟空浏览器")
                    start_app(self.device_id, self.app_name)
            # 如果有再看那就点击再看
            stats, box, result = find_screen_text_position(self.device_id, "再看一", top_normal_bottom="top")
            if stats:
                print_help_text(self.device_id, "再看一")
                position = find_screen_by_result(result, "再看一")
                tap(self.device_id, position)
                continue
            else:
                # 关闭广告
                stats, box, result = find_screen_text_position(self.device_id, "关闭")
                print_help_text(self.device_id, "关闭广告")
                position = find_screen_by_result(result, "关闭")
                if position:
                    tap(self.device_id, position)
                else:
                    position = find_screen_by_result(result, "X")
                    if position:
                        tap(self.device_id, position)
                    else:
                        press_back(self.device_id)
                # 如果有再看 那就点击再看
                stats, position = find_screen_text_button_position(self.device_id, "再看一", "再看一")
                if stats:
                    print_help_text(self.device_id, "点击看下一")
                    tap(self.device_id, position)
                    continue
            self.back_to_main()
            break

    def auto_coin_box(self):
        # 看宝箱的广告
        print_help_text(self.device_id, "点击任务菜单，开始看宝箱广告")
        # 点击任务菜单
        self.back_to_main()
        tap(self.device_id, self.coin_button)
        self.rm_ad()
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            print_help_text(self.device_id, "开宝箱")
            # 点击宝箱
            tap(self.device_id, position)
            time.sleep(1)
            # 点击”看视频再领“ 开始看广告
            stats, position = find_screen_text_button_position(self.device_id, "看视频再", "看视频再")
            if stats:
                tap(self.device_id, position)
                # 循环查看
                self.ad()
        else:
            print_help_text(self.device_id, "目前不能点击宝箱！")

    # 看广告
    def auto_watch_ad(self):
        # 点击任务菜单
        self.back_to_main()
        tap(self.device_id, self.coin_button)
        self.rm_ad()
        self.back_top()
        print_help_text(self.device_id, "点击任务菜单,开始看广告")
        tap(self.device_id, self.coin_button)
        # 上滑找“看广告” 最多5次
        for i in range(3):
            status, position = find_screen_text_button_position(self.device_id, "看广告视频", "去完成")
            if status:
                print_help_text(self.device_id, "看广告")
                tap(self.device_id, position)
                self.ad()
                return True
            # 上滑
            up_long_swipe(self.device_id)
        print_help_text(self.device_id, "未找到看广告领福利的位置！")

    def watch_small_video(self):
        # 看小视频
        self.back_to_main()
        # 点击视频
        stats, position = find_screen_text_button_position(self.device_id, "视频", "视频", top_normal_bottom="bottom")
        if stats:
            print_help_text(self.device_id, "开始刷视频")
            tap(self.device_id, position)
            for i in range(25):
                print_help_text(self.device_id, "刷小视频第%s\%s次" % (str(i), 10))
                time.sleep(get_random_time(4, 6))
                up_long_swipe(self.device_id)

    # 开始自动刷app
    def auto_run(self, light_screen_stats=True, watch_small_video=True, watch_ad=True, coin_box=True):
        # 解锁屏幕
        if light_screen_stats:
            print_help_text(self.device_id, "解锁设备")
            unlock_device(self.device_id)
        # 启动app
        self.start_wk_app()
        time.sleep(1)
        # 获取当前收益
        coin_start, cash_start = self.get_coin_num()
        # 看小视频
        if watch_small_video:
            self.watch_small_video()
        # 看广告
        if watch_ad:
            self.auto_watch_ad()
        # 开宝箱
        if coin_box:
            self.auto_coin_box()
        # 获取当前收益
        coin_end, cash_end = self.get_coin_num()
        self.coin_current = coin_end - coin_start
        self.cash_current = round(self.coin_current / 33000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end


if __name__ == "__main__":
    wukong_obj = WuKongOpt("192.168.101.106:5555")
    wukong_obj.auto_run()