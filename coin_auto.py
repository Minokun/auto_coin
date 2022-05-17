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
        self.app_name = "article_lite"
        self.first_page_menu_position = (110, 2330)
        self.tuijian_menu_position = (250, 320)
        self.coin_menu_position = (550, 2330)
        self.coin_box_position = (900, 2130)
        self.ads_position = (550, 1450)
        self.ads_shut = (975, 160)

    def start_article_app(self):
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            start_app(device_id, self.app_name)
            # 启动后识别屏幕顶部 如果有跳过广告 则点击
            jump_ad = False
            if jump_ad:
                png_name = screen_cap(device_id)
                local_png_path = screen_pull(png_name)
                self.paddle_detect.detect_top(local_png_path)
                for i in self.paddle_detect.top_list:
                    if i[1][0].find("跳过广告") >= 0:
                        position_x = i[0][1][0] - 20
                        position_y = i[0][1][1] + 10
                        print("********** 跳过启动页广告 ********** ")
                        tap(device_id, (position_x, position_y))
                        break

    def shut_app(self):
        # 关掉app
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            shut_app(device_id, self.app_name)

    def back_to_main(self):
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            # 回到首页
            # 截屏识别是否有首页 没有则发送返回
            png_name = screen_cap(device_id=device_id)
            local_png_path = screen_pull(png_name)
            self.paddle_detect.detect_bottom(local_png_path)

    # 广告是否结束
    def ad_end(self, device_id):
        # 截屏
        print("********** 截屏 ********** ")
        png_name = screen_cap(device_id)
        # 拷贝到本地
        print("********** 拷贝图片 ********** ")
        local_png_path = screen_pull(png_name)
        # ocr识别
        print("********** ocr识别 ********** ")
        self.paddle_detect.detect_bottom(local_png_path)
        # 如果底部菜单有首页 则看完了
        status, _, _ = find_screen_text_position(device_id, "首页")
        if status:
            print("********** 结束本次广告视频！ ********** ")
        else:
            print("********** 继续看广告...... ********** ")
        return status

    # 看广告
    def watch_ad(self, device_id):
        status = False
        while not status:
            time.sleep(15)
            # 如果有 查看详情 立即下载的按钮 则先点击后在返回
            check_status, box, _ = find_screen_text_position(device_id, "立即下载")
            if check_status:
                position = (box[0][0] + 15, box[0][1] + 15)
                print("******** 点击查看详情 *********")
                tap(device_id, position)
                time.sleep(1)
                print("******** 返回 *********")
                press_back(device_id)
            # 点击关闭
            print("********** 点击关闭 ********** ")
            tap(device_id, self.ads_shut)
            # 广告是否看完
            status = self.ad_end(device_id)
            # 没看完
            if not status:
                tap(device_id, self.ads_position)

    # 获取开宝箱的位置
    def get_coin_box_position(self, device_id):
        png_name = screen_cap(device_id)
        local_png_path = screen_pull(png_name)
        self.paddle_detect.detect(local_png_path)
        position = False
        for i in self.paddle_detect.bottom_list:
            if i[1][0].find("得金币") > 0:
                position = i[0][0]
        return position

    def browser_article(self, time_period=900000):
        # 浏览文章
        @multiple_device(device_list=self.device_id_list, time_period=time_period)
        def _opt(device_id, time_period):
            per_time = 6000
            num = math.ceil(time_period / per_time)
            print("********** 将循环浏览%s次 ********** " % str(num))
            # 点击首页等2s
            tap(device_id, self.first_page_menu_position)
            time.sleep(1)
            print("********** 点击推荐 ********** ")
            # 点击推荐
            tap(device_id, self.tuijian_menu_position)
            for i in range(num):
                print("第%s次" % str(i+1))
                # 开始滑动浏览
                up_short_swipe(device_id)
                time.sleep(get_random_time())

    def auto_coin_box(self):
        # 看宝箱的广告
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            # 点击任务菜单
            print("********** 点击任务菜单，开始看宝箱广告 ********** ")
            tap(device_id, self.coin_menu_position)
            # 返会再点击一次 为了防止布局不一样
            press_back(device_id)
            tap(device_id, self.coin_menu_position)
            # 点击宝箱
            print('********** 点击宝箱 ********** ')
            coin_box_position = self.get_coin_box_position(device_id)
            coin_box_position = coin_box_position if coin_box_position else self.coin_box_position
            tap(device_id, coin_box_position)
            time.sleep(0.5)
            # 点击查看视频
            tap(device_id, self.ads_position)
            # 循环查看
            self.watch_ad(device_id)

    # 看广告
    def auto_watch_ad(self):
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            # 点击任务菜单
            print("********** 点击任务菜单,开始开广告 ********** ")
            tap(device_id, self.coin_menu_position)
            # 返会再点击一次 为了防止布局不一样
            press_back(device_id)
            tap(device_id, self.coin_menu_position)
            # 上滑找“看广告” 最多5次
            for i in range(5):
                # 上滑
                up_long_swipe(device_id)
                status, box, result = find_screen_text_position(device_id, "看广告")
                if status:
                    y_ad = box[0][1]
                    # 获取“领福利”的 xy
                    for i in result:
                        # 如果找到了该位置
                        if i[1][0].find("领福利") >= 0 and i[0][2][1] >= y_ad:
                            print("********** 点击看广告！ ********** ")
                            x, y = i[0][0][0] + 15, i[0][0][1] + 15
                            tap(device_id, (x, y))
                            self.watch_ad(device_id)
                            break
                    break
                else:
                    print("********** 未找到 看广告领福利 的位置！ ********** ")

    # 点亮屏幕
    def light_screen(self):
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            light_screen(device_id)
            up_short_swipe(device_id)
            input_text(device_id, "910729")

    # 开始自动刷app
    def auto_article_lite(self, light_screen=False, read_article=False, watch_coin_box=False, watch_ad=False):
        # 点亮屏幕
        if light_screen:
            self.light_screen()
        # 启动app
        self.start_article_app()
        time.sleep(1)
        if read_article:
            # 浏览首页阅读文章
            self.browser_article(time_period=500000)
        if watch_coin_box:
            # 开宝箱
            self.auto_coin_box()
        if watch_ad:
            # 看广告
            self.auto_watch_ad()

    # 看一分钟小视频
    def look_small_video(self):
        # 到首页
        pass

    # 逛商品90s
    def look_goods(self):
        pass

if __name__ == "__main__":
    # 如果没有设备 则重启adb 服务
    if len(CurrentDeviceList) == 0:
        print("重启adb服务")
        reboot_adb()
    else:
        print("本次连接设备：")
        [print(i) for i in CurrentDeviceList]
    # 今日头条极速版刷金币
    article_lite_opt = ArticleLiteOpt()
    article_lite_opt.auto_article_lite(light_screen=False, read_article=False, watch_coin_box=False, watch_ad=True)