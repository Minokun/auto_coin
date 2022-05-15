# -*- coding:utf-8 -*-
import math
import sys
import time

from phone_opt import *
from paddle_opt import *


# 抖音极速版
class DouYinOpt:
    def __init__(self):
        self.device_id_list = get_all_device_id()
        self.coin_menu_position = (550, 2330)
        self.add_start_position = (550, 1450)
        self.add_internal_time = 32
        self.add_shut_menu_position = (980, 155)

    def press_main_coin(self):
        for device_id in self.device_id_list:
            tap(device_id, self.coin_menu_position)

# 今日头条极速版
class ArticleLiteOpt:
    def __init__(self):
        self.device_id_list = get_all_device_id()
        self.paddle_detect = DetectPic()
        self.first_page_menu_position = (110, 2330)
        self.tuijian_menu_position = (250, 320)
        self.coin_menu_position = (550, 2330)
        self.coin_box_position = (900, 2130)
        self.ads_position = (550, 1450)
        self.ads_shut = (975, 160)

    def start_article_app(self):
        def _opt(device_id):
            start_app(device_id, "article_lite")
            # 启动后识别屏幕顶部 如果有跳过广告 则点击
            time.sleep(2)
            png_name = screen_cap(device_id)
            local_png_path = screen_pull(png_name)
            self.paddle_detect.detect_top(local_png_path)
            for i in self.paddle_detect.top_list:
                if i[1][0].find("跳过广告") >= 0:
                    position_x = i[0][1][0] - 20
                    position_y = i[0][1][1] + 10
                    print("跳过启动页广告")
                    tap(device_id, (position_x, position_y))
                    break

        for device_id in self.device_id_list:
            _opt(device_id)

    def ad_end(self, device_id):
        # 截屏
        print("截屏")
        png_name = screen_cap(device_id)
        # 拷贝到本地
        print("拷贝图片")
        local_png_path = screen_pull(png_name)
        # ocr识别
        print("ocr识别")
        self.paddle_detect.detect_bottom(local_png_path)
        # 如果底部菜单有首页 则看完了
        status = True
        for i in self.paddle_detect.bottom_list:
            if i[1][0].find("首页") >= 0:
                status = False
                break
        return status

    def get_coin_box_position(self, device_id):
        png_name = screen_cap(device_id)
        local_png_path = screen_pull(png_name)
        self.paddle_detect.detect(local_png_path)
        position = False
        for i in self.paddle_detect.bottom_list:
            if i[1][0].find("得金币") > 0:
                position = i[0][0]
        return position

    def browser_article(self, time_period=15000 * 60):
        # 浏览文章
        def _opt(device_id, time_period):
            per_time = 2 * 60 * 1000
            num = math.floor(time_period / per_time)
            print("即将总共循环浏览%s次" % str(num + 1))
            n = 1
            for i in range(num):
                print("第%s次" % str(n))
                n += 1
                # 点击首页等2s
                tap(device_id, self.first_page_menu_position)
                time.sleep(2)
                print("点击推荐")
                # 点击推荐
                tap(device_id, self.tuijian_menu_position)
                time.sleep(2)
                for j in range(20):
                    # 开始滑动浏览
                    up_short_swipe(device_id)
                    time.sleep(get_random_time())

        for device_id in self.device_id_list:
            _opt(device_id, time_period)

    def coin_box(self):
        # 看宝箱的广告
        def _opt(device_id):
            # 点击菜单的开宝箱按钮
            print("点击开宝箱菜单")
            tap(device_id, self.coin_menu_position)
            # 返会再点击一次 为了防止布局不一样
            press_back(device_id)
            tap(device_id, self.coin_menu_position)
            # 点击宝箱
            print('点击宝箱')
            coin_box_position = self.get_coin_box_position(device_id)
            coin_box_position = coin_box_position if coin_box_position else self.coin_box_position
            tap(device_id, coin_box_position)
            status = True
            while status:
                # 点击看视频
                tap(device_id, self.ads_position)
                time.sleep(18)
                # 点击关闭
                print("点击关闭")
                tap(device_id, self.ads_shut)
                # 广告是否看完
                status = self.ad_end(device_id)

        for device_id in self.device_id_list:
            _opt(device_id)

def auto_article_lite():
    # 今日头条极速版刷金币
    article_lite_opt = ArticleLiteOpt()
    # 启动app
    article_lite_opt.start_article_app()
    time.sleep(2)
    # 浏览首页阅读文章
    # article_lite_opt.browser_article(time_period=3 * 60 * 1000)
    # 开宝箱
    article_lite_opt.coin_box()
    article_lite_opt.browser_article(time_period=3 * 60 * 1000)


if __name__ == "__main__":
    auto_article_lite()