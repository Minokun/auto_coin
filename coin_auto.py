# -*- coding:utf-8 -*-
import math
import time

from phone_opt import *


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
        self.first_page_menu_position = (110, 2330)
        self.tuijian_menu_position = (250, 320)

    def start_article_app(self):
        for device_id in self.device_id_list:
            start_app(device_id, "article_lite")

    def browser_article(self, time_period=15000 * 60):
        per_time = 2 * 60 * 1000
        num = math.floor(time_period / per_time)
        print("即将总共循环浏览%s次" % str(num + 1))
        n = 1
        for device_id in self.device_id_list:
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


def auto_article_lite():
    # 今日头条极速版刷金币
    article_lite_opt = ArticleLiteOpt()
    # 启动app
    article_lite_opt.start_article_app()
    time.sleep(2)
    # 浏览首页阅读文章
    article_lite_opt.browser_article()


if __name__ == "__main__":
    auto_article_lite()