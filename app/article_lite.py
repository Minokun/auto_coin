# -*- coding:utf-8 -*-
import math, re
import time
from config import TIMES

from utils.phone_opt import *


# 今日头条极速版
class ArticleLiteOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "article_lite"
        self.app_name_chinese = app_name[self.app_name]
        self.current_step = ''
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        # 底部菜单的首页按钮坐标
        self.first_page_menu_position = (110, int(2330 * self.height_scale))
        self.coin_task_position = (550, int(2330 * self.height_scale))
        # 首页上边菜单栏的推荐按钮坐标
        self.tuijian_menu_position = (250, int(320 * self.height_scale))
        # 首页上边菜单栏的全部按钮坐标
        self.main_task_position = (1000, int(320 * self.height_scale))
        # 点击弹出的中间看广告按钮坐标
        self.ads_position = (550, int(1500 * self.height_scale))
        # 看完广告关闭按钮
        self.ads_shut = (975, int(160 * self.height_scale))
        # 当前金币和现金收益
        self.coin_current = 0.0
        self.cash_current = 0.0
        self.coin_today = 0.0
        self.cash_total = 0.0

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
        status, position = find_screen_text_button_position(self.device_id, "我知道", "我知道")
        if status:
            tap(self.device_id, position)
        status, box, result = find_screen_text_position(self.device_id, "翻倍领取")
        if status:
            position = find_screen_by_result(result, "翻倍领取")
            tap(self.device_id, position)
        position = find_screen_by_result(result, "额外领取")
        if position:
            tap(self.device_id, position)
        position = find_screen_by_result(result, "继续阅读")
        if position:
            tap(self.device_id, position)

    # 上滑到最顶部
    def back_top(self):
        for i in range(4):
            down_long_swipe(self.device_id)

    def get_coin_num(self):
        print_help_text(self.device_id, "获取当前收益")
        # 点击任务
        tap(self.device_id, self.coin_task_position)
        time.sleep(1.5)
        status, position = find_screen_text_button_position(self.device_id, "翻倍领取", "翻倍领取")
        if status:
            tap(self.device_id, position)
            self.watch_ad()
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
                stats, box, result = find_screen_text_position(self.device_id, "再看一")
                if stats:
                    position = find_screen_by_result(result, "再看一")
                    print_help_text(self.device_id, "再看一")
                    tap(self.device_id, position)
                    self.watch_ad()
                else:
                    position = find_screen_by_result(result, "继续")
                    if position:
                        tap(self.device_id, position)
                    else:
                        press_back(self.device_id)
            time.sleep(1)
            if i > 4:
                self.shut_app()
                time.sleep(1)
                self.start_article_app()
                break

    # 看广告
    def watch_ad(self):
        status = False
        while not status:
            time.sleep(20)
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
                    print_help_text(self.device_id, "跳回到今日头条")
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
                tap(self.device_id, self.ads_shut)
                # 如果有再看 那就点击再看
                stats, position = find_screen_text_button_position(self.device_id, "再看一", "再看一")
                if stats:
                    print_help_text(self.device_id, "点击看下一")
                    tap(self.device_id, position)
                    continue
            self.back_to_main()
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
            time.sleep(2)
            stats, position = find_screen_text_button_position(self.device_id, "首页", "首页", top_normal_bottom="bottom")
            if not stats:
                print_help_text(self.device_id, '不在首页，回到首页')
                press_back(self.device_id)
                continue
            print_help_text(self.device_id, "第%s/%s次" % (str(i + 1), str(num)))
            # 开始滑动浏览 每天第一次短刷 其他长刷
            if first_stats:
                up_short_swipe(self.device_id)
            else:
                up_long_swipe(self.device_id)
            time.sleep(0.5)
            # 检测 如果有阅读惊喜奖励 领金币
            status, position = find_screen_text_button_position(self.device_id, "阅读惊喜奖励", "领金币")
            if status:
                print_help_text(self.device_id, "发现阅读惊喜奖励 开始领金币")
                tap(self.device_id, position)
                time.sleep(1)
                stats, position = find_screen_text_button_position(self.device_id, "再领", "再领")
                if stats:
                    print_help_text(self.device_id, "点击看广告")
                    tap(self.device_id, position)
                    self.watch_ad()
                else:
                    press_back(self.device_id)
            # 如果是第一次做活跃则慢慢刷 其他直接找阅读惊喜奖励
            if first_stats:
                time.sleep(get_random_time())

    def auto_coin_box(self):
        # 看宝箱的广告
        print_help_text(self.device_id, "点击任务菜单，开始看宝箱广告")
        # 点击任务菜单
        self.back_to_main()
        tap(self.device_id, self.coin_task_position)
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
        tap(self.device_id, self.coin_task_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(self.device_id)
        tap(self.device_id, self.coin_task_position)
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
        tap(self.device_id, self.main_task_position)
        time.sleep(1.5)
        # 找小视频
        status, box, _ = find_screen_text_position(self.device_id, "小视频")
        if not status:
            return False
        # 点击小视频
        position = (box[0][0] + 10, box[0][1] + 10)
        tap(self.device_id, position)
        time.sleep(1)
        # 点击一个视频
        tap(self.device_id, (300, 720))
        print_help_text(self.device_id, "开始看小视频")
        if self.device_id in TIMES[self.app_name]['watch_small_video'].keys():
            num = TIMES[self.app_name]['watch_small_video'][self.device_id]
        else:
            num = TIMES[self.app_name]['watch_small_video']['default']
        for i in range(num):
            print_help_text(self.device_id, "第%s/30次" % str(i + 1))
            up_short_swipe(self.device_id)
            time.sleep(get_random_time(6, 10))
        # 返回
        press_back(self.device_id)
        # 点击任务栏
        tap(self.device_id, self.main_task_position)
        # 找推荐
        status, box, _ = find_screen_text_position(self.device_id, "推荐")
        if not status:
            self.shut_app()
            time.sleep(1)
            self.start_article_app()
            return True
        position = (box[0][0] + 10, box[0][1] + 10)
        tap(self.device_id, position)

    # 逛商品90s （6分钟一次）
    def auto_watch_goods(self):
        # 点击任务菜单
        self.back_to_main()
        print_help_text(self.device_id, "点击任务菜单,开始逛商品")
        tap(self.device_id, self.coin_task_position)
        # 返会再点击一次 为了防止布局不一样
        press_back(self.device_id)
        tap(self.device_id, self.coin_task_position)
        # 上滑找“逛商场” 最多5次
        for i in range(3):
            # 上滑
            up_long_swipe(self.device_id)
            status, position = find_screen_text_button_position(self.device_id, "逛商品", "去领取")
            if status:
                # 点击
                tap(self.device_id, position)
                # 开始刷15次
                for n in range(20):
                    number = n + 1
                    print_help_text(self.device_id, "第%s/20次" % number)
                    up_long_swipe(self.device_id)
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
        # 获取当前收益
        coin_start, cash_start = self.get_coin_num()
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
            print_help_text(self.device_id, "开始看广告")
            self.auto_watch_ad()
        if watch_goods:
            # 逛商品
            self.auto_watch_goods()
        # 获取当前收益
        coin_end, cash_end = self.get_coin_num()
        self.coin_current = coin_end - coin_start
        self.cash_current = round(self.coin_current / 33000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end


if __name__ == "__main__":
    article_obj = ArticleLiteOpt("192.168.101.103:5555")

    article_obj.get_coin_num()
