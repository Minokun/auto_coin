# -*- coding:utf-8 -*-
import math
import time

from phone_opt import *


# 今日头条极速版
class ArticleLiteOpt:
    def __init__(self, device_id):
        self.device_id = device_id
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

    def start_article_app(self):
        print_help_text(self.device_id, "启动今日头条极速版")
        # 启动今日头条极速版
        start_app(self.device_id, self.app_name)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)

    def shut_app(self):
        shut_app(self.device_id, self.app_name)

    def back_to_main(self):
        for i in range(6):
            print_help_text(self.device_id, "回到首页")
            status, position = find_screen_text_button_position(self.device_id, "首页", "首页")
            # 如果有就退出
            if status:
                tap(self.device_id, position)
                break
            else:
                press_back(self.device_id)
            time.sleep(1)

    # 看广告
    def watch_ad(self):
        print_help_text(self.device_id, "开始看广告")
        status = False
        while not status:
            time.sleep(20)
            # 如果有 查看详情 立即下载的按钮 则先点击后在返回
            check_status, box, result = find_screen_text_position(self.device_id, "下载")
            check_position = find_screen_by_result(result, '查看详情')
            xz_position = find_screen_by_result(result, "立即下载")
            button_position = check_position if check_position else xz_position
            tm_position = find_screen_by_result(result, "天猫")
            tb_position = find_screen_by_result(result, "淘宝")
            jd_position = find_screen_by_result(result, "京东")
            mt_position = find_screen_by_result(result, "美团")
            position = () if (tm_position or tb_position or jd_position or mt_position or not button_position) else button_position
            if position:
                print_help_text(self.device_id, "点击查看详情")
                tap(self.device_id, position)
                time.sleep(1)
                for i in range(3):
                    up_long_swipe(self.device_id)
                    time.sleep(1)
                print_help_text(self.device_id, "返回")
                press_back(self.device_id)
            # 按理说应该在广告页的 所以应该有广告两个字没有 就跳回
            gg_stats, gg_position = find_screen_text_button_position(self.device_id, "广告", "广告")
            if not gg_position:
                print_help_text(self.device_id, "跳回到今日头条极速版")
                press_back(self.device_id)
                press_back(self.device_id)
            # 如果有再看视频 点击再看
            zk_position = find_screen_by_result(result, "再看")
            # 新版 如果有再看就点击再看
            if zk_position:
                print_help_text(self.device_id, "继续看下一个")
                tap(self.device_id, zk_position)
                continue
            # 如果有坚持再看
            jczk_position = find_screen_by_result(result, "坚持再看")
            if jczk_position:
                print_help_text(self.device_id, "继续看下一个")
                tap(self.device_id, jczk_position)
                continue
            # 都没有就点击右上角的X
            print_help_text(self.device_id, "关掉当前广告")
            tap(self.device_id, self.ads_shut)
            # 看是否广告看完了
            status, _ = find_screen_text_button_position(self.device_id, "首页", "首页")
            if not status:
                # 老版本 还得点一下看广告
                print_help_text(self.device_id, "继续看下一个")
                tap(self.device_id, self.ads_position)
            else:
                break


    def browser_article(self, first_stats=False):
        self.back_to_main()
        # 浏览文章
        if first_stats:
            time_period = 800000
        else:
            time_period = 80000
        per_time = 8000
        num = math.ceil(time_period / per_time)
        print_help_text(self.device_id, "将循环浏览%s次" % str(num))
        # 点击推荐
        tap(self.device_id, self.tuijian_menu_position)
        for i in range(num):
            print_help_text(self.device_id, "第%s/%s次" % (str(i + 1), str(num)))
            # 开始滑动浏览 每天第一次短刷 其他长刷
            if first_stats:
                up_short_swipe(self.device_id)
            else:
                up_long_swipe(self.device_id)
            # 检测 如果有阅读惊喜奖励 领金币
            status, position = find_screen_text_button_position(self.device_id, "阅读惊喜奖励", "领金币")
            if status:
                print_help_text(self.device_id, "发现阅读惊喜奖励 开始领金币")
                tap(self.device_id, position)
                time.sleep(1)
                print_help_text(self.device_id, "点击看广告")
                tap(self.device_id, self.ads_position)
                print_help_text(self.device_id, "开始看广告")
                self.watch_ad()
            # 如果是第一次做活跃则慢慢刷 其他直接找阅读惊喜奖励
            if first_stats:
                time.sleep(get_random_time())

    def auto_coin_box(self):
        # 看宝箱的广告
        print_help_text(self.device_id, "点击任务菜单，开始看宝箱广告")
        # 点击任务菜单
        self.back_to_main()
        tap(self.device_id, self.coin_menu_position)
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
        tap(self.device_id, self.coin_menu_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(self.device_id)
        tap(self.device_id, self.coin_menu_position)
        # 上滑找“看广告” 最多5次
        for i in range(3):
            # 上滑
            up_long_swipe(self.device_id)
            status, position = find_screen_text_button_position(self.device_id, "看广告", "领福利")
            if status:
                print_help_text(self.device_id, "看广告")
                tap(self.device_id, position)
                self.watch_ad()
                return True
        print_help_text(self.device_id, "未找到看广告领福利的位置！")

    # 看一分钟小视频
    def auto_watch_small_video(self):
        self.back_to_main()
        print_help_text(self.device_id, "点击任务菜单，开始看小视频")
        tap(self.device_id, self.first_page_menu_position)
        print_help_text(self.device_id, "点击首页任务栏")
        tap(self.device_id, (1000, 320))
        # 找小视频
        status, box, _ = find_screen_text_position(self.device_id, "小视频")
        # 点击小视频
        position = (box[0][0] + 10, box[0][1] + 10)
        tap(self.device_id, position)
        time.sleep(1)
        # 点击一个视频
        tap(self.device_id, (300, 720))
        print_help_text(self.device_id, "开始看小视频")
        for i in range(12):
            print_help_text(self.device_id, "第%s/12次" % str(i + 1))
            up_short_swipe(self.device_id)
            time.sleep(get_random_time())
        # 返回
        press_back(self.device_id)
        # 点击任务栏
        tap(self.device_id, self.main_task_position)
        # 找推荐
        status, box, _ = find_screen_text_position(self.device_id, "推荐")
        position = (box[0][0] + 10, box[0][1] + 10)
        tap(self.device_id, position)

    # 逛商品90s （6分钟一次）
    def auto_watch_goods(self):
        # 点击任务菜单
        self.back_to_main()
        print_help_text(self.device_id, "点击任务菜单,开始逛商品")
        tap(self.device_id, self.coin_menu_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(self.device_id)
        tap(self.device_id, self.coin_menu_position)
        # 上滑找“逛商场” 最多5次
        for i in range(3):
            # 上滑
            up_long_swipe(self.device_id)
            status, position = find_screen_text_button_position(self.device_id, "逛商品", "去领取")
            if status:
                # 点击
                tap(self.device_id, position)
                # 开始刷15次
                for n in range(13):
                    number = n + 1
                    print_help_text(self.device_id, "第%s/13次" % number)
                    up_short_swipe(self.device_id)
                    time.sleep(get_random_time())
                # 返回
                press_back(self.device_id)
                return True
        print_help_text(self.device_id, "未找到逛商品的位置！")

    # TODO 自动领取所有奖励
    def auto_take_award(self):
        pass

    # 开始自动刷app
    def auto_run(self, first_status=True, light_screen_stats=True, read_article=True, watch_small_video=True,
                          watch_coin_box=True, watch_ad=True,
                          watch_goods=True):
        # 解锁屏幕
        if light_screen_stats:
            print_help_text(self.device_id, "解锁设备")
            unlock_device(self.device_id)
        # 启动app
        self.start_article_app()
        time.sleep(1)
        if read_article:
            # 浏览首页阅读文章
            self.browser_article(first_status)
        if watch_small_video:
            # 看小视频
            self.auto_watch_small_video()
        if watch_coin_box:
            # 开宝箱
            self.auto_coin_box()
        if watch_ad:
            # 看广告
            self.auto_watch_ad()
        if watch_goods:
            # 逛商品
            self.auto_watch_goods()


if __name__ == "__main__":
    article_obj = ArticleLiteOpt("192.168.101.101:5555")
    article_obj.auto_run(first_status=False, light_screen_stats=False, read_article=False, watch_small_video=False,
                                  watch_coin_box=True, watch_ad=True, watch_goods=False)
