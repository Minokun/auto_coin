# -*- coding:utf-8 -*-
import math
from phone_opt import *
from paddle_opt import *


# 今日头条极速版
class ArticleLiteOpt:
    def __init__(self):
        self.device_id_list = get_all_device_id()
        self.paddle_detect = paddle_ocr_obj
        self.app_name = "article_lite"
        # 底部菜单的首页按钮坐标
        self.first_page_menu_position = (110, 2330)
        # 首页上边菜单栏的推荐按钮坐标
        self.tuijian_menu_position = (250, 320)
        # 首页底部菜单栏的开宝箱按钮坐标
        self.coin_menu_position = (550, 2330)
        # 首页上边菜单栏的全部按钮坐标
        self.main_task_position = (1000, 320)
        # 任务界面的宝箱坐标
        self.coin_box_position = (900, 2130)
        # 点击弹出的中间看广告按钮坐标
        self.ads_position = (550, 1450)
        # 看完广告关闭按钮
        self.ads_shut = (975, 160)

    def start_article_app(self, device_id):
        print(" ************ 启动今日头条极速版 *************")
        # 启动今日头条极速版
        start_app(device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(device_id, "跳过广告", "跳过广告")
            if status:
                tap(device_id, position)

    def shut_app(self, device_id):
        shut_app(device_id, self.app_name)

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
            check_status, box, _ = find_screen_text_position(device_id, "下载")
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

    def browser_article(self, device_id, time_period=900000):
        # 浏览文章
        per_time = 8000
        num = math.ceil(time_period / per_time)
        print("********** 将循环浏览%s次 ********** " % str(num))
        # 点击首页等2s
        tap(device_id, self.first_page_menu_position)
        time.sleep(1)
        print("********** 点击推荐 ********** ")
        # 点击推荐
        tap(device_id, self.tuijian_menu_position)
        for i in range(num):
            print("第%s次" % str(i + 1))
            # 开始滑动浏览
            up_short_swipe(device_id)
            # 检测 如果有阅读惊喜奖励 领金币
            status, position = find_screen_text_button_position(device_id, "阅读惊喜奖励", "领金币")
            if status:
                print("发现阅读惊喜奖励 开始领金币")
                tap(device_id, position)
                time.sleep(0.5)
                print("点击看广告")
                tap(device_id, self.ads_position)
                print("开始看广告")
                self.watch_ad(device_id)
            time.sleep(get_random_time())

    def auto_coin_box(self, device_id):
        # 看宝箱的广告
        # 点击任务菜单
        print("********** 点击任务菜单，开始看宝箱广告 ********** ")
        tap(device_id, self.coin_menu_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(device_id)
        tap(device_id, self.coin_menu_position)
        # 点击宝箱
        print('********** 点击宝箱 ********** ')
        status, position = find_screen_text_button_position(device_id, "开宝箱得金币", "开宝箱得金币")
        coin_box_position = position if status else self.coin_box_position
        tap(device_id, coin_box_position)
        time.sleep(0.5)
        # 点击查看视频
        tap(device_id, self.ads_position)
        # 循环查看
        self.watch_ad(device_id)

    # 看广告
    def auto_watch_ad(self, device_id):
        # 点击任务菜单
        print("********** 点击任务菜单,开始看广告 ********** ")
        tap(device_id, self.coin_menu_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(device_id)
        tap(device_id, self.coin_menu_position)
        # 上滑找“看广告” 最多5次
        for i in range(5):
            # 上滑
            up_long_swipe(device_id)
            status, position = find_screen_text_button_position(device_id, "看广告", "领福利")
            if status:
                print("************ 开始看广告 *************")
                tap(device_id, position)
                self.watch_ad(device_id)
                return True
        print("********** 未找到 看广告领福利 的位置！ ********** ")

    # 看一分钟小视频
    def auto_watch_small_video(self, device_id):
        print("********** 点击任务菜单，开始看小视频 ********** ")
        tap(device_id, self.first_page_menu_position)
        print("********** 点击首页任务栏 ********** ")
        tap(device_id, (1000, 320))
        # 找小视频
        status, box, _ = find_screen_text_position(device_id, "小视频")
        # 点击小视频
        position = (box[0][0] + 10, box[0][1] + 10)
        tap(device_id, position)
        time.sleep(1)
        # 点击一个视频
        tap(device_id, (300, 720))
        print("开始看小视频")
        for i in range(12):
            print("******** 第%s/15次 **************" % str(i))
            up_short_swipe(device_id)
            time.sleep(get_random_time())
        # 返回
        press_back(device_id)
        # 点击任务栏
        tap(device_id, self.main_task_position)
        # 找推荐
        status, box, _ = find_screen_text_position(device_id, "推荐")
        position = (box[0][0] + 10, box[0][1] + 10)
        tap(device_id, position)

    # 逛商品90s （6分钟一次）
    def auto_watch_goods(self, device_id):
        # 点击任务菜单
        print("********** 点击任务菜单,开始逛商品 ********** ")
        tap(device_id, self.coin_menu_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(device_id)
        tap(device_id, self.coin_menu_position)
        # 上滑找“逛商场” 最多5次
        for i in range(5):
            # 上滑
            up_long_swipe(device_id)
            status, position = find_screen_text_button_position(device_id, "逛商品", "去领取")
            if status:
                # 点击
                tap(device_id, position)
                # 开始刷15次
                for n in range(13):
                    number = n + 1
                    print("******* 第%s/13次 ********" % number)
                    up_short_swipe(device_id)
                    time.sleep(get_random_time())
                # 返回
                press_back(device_id)
                return True
        print("********** 未找到 逛商品 的位置！ ********** ")

    # TODO 自动领取所有奖励
    def auto_take_award(self):
        pass

    # 开始自动刷app
    def auto_run(self, light_screen_stats=True, read_article=True, watch_small_video=True,
                          watch_coin_box=True, watch_ad=True,
                          watch_goods=True):
        @multiple_device(device_list=self.device_id_list)
        def _opt(device_id):
            # 解锁屏幕
            if light_screen_stats:
                print("******** 解锁设备 **********")
                unlock_device(device_id)
            # 启动app
            self.start_article_app(device_id)
            time.sleep(1)
            if read_article:
                # 浏览首页阅读文章
                self.browser_article(device_id, time_period=30000)
            if watch_small_video:
                # 看小视频
                self.auto_watch_small_video(device_id)
            if watch_ad:
                # 看广告
                self.auto_watch_ad(device_id)
            if watch_coin_box:
                # 开宝箱
                self.auto_coin_box(device_id)
            if watch_goods:
                # 逛商品
                self.auto_watch_goods(device_id)