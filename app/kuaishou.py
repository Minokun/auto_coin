# -*- coding:utf-8 -*-
import time

from utils.phone_opt import *


# 抖音极速版
class KuaiShouOpt:
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "kuaishou"
        self.app_name_chinese = app_name[self.app_name]
        self.current_step = ''
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        # 首页
        self.main_position = (100, int(2330 * self.height_scale))
        # 去赚钱
        self.task_position = (780, int(2300 * self.height_scale))
        # 关闭广告的按键
        self.ad_shut = (980, int(150 * self.height_scale))
        # 看广告中间的继续按钮
        self.ad_continue_menu_position = (530, int(1380 * self.height_scale))
        # 点击宝箱中间得看广告视频
        self.coin_box_ad = (520, int(1450 * self.height_scale))
        # 左上角已完成广告按钮
        self.ad_end = (280, int(170 * self.height_scale))
        # 当前金币和现金收益
        self.coin_current = 0.0
        self.cash_current = 0.0
        self.coin_today = 0.0
        self.cash_total = 0.0

    def start_kuaishou_app(self):
        start_app(self.device_id, self.app_name)
        time.sleep(2)
        # 启动后识别屏幕顶部 如果有跳过广告 则点击
        jump_ad = False
        if jump_ad:
            time.sleep(0.5)
            status, position = find_screen_text_button_position(self.device_id, "跳过", "跳过")
            if status:
                tap(self.device_id, position)
        # 青少年模式
        stats, box, result = find_screen_text_position(self.device_id, "我知道了")
        if stats:
            position = find_screen_by_result(result, "我知道了")
            tap(self.device_id, position)
        position = find_screen_by_result(result, '点击翻倍')
        if position:
            tap(self.device_id, position)

    def shut_app(self):
        shut_app(self.device_id, self.app_name)

    def get_coin_num(self):
        print_help_text(self.device_id, "获取当前收益")
        self.back_main_coin()
        # 点击去赚钱
        tap(self.device_id, self.task_position)
        time.sleep(1)
        self.rm_ad()
        time.sleep(1)
        self.back_top()
        stats, box, result = find_screen_text_position(self.device_id, "我的抵用金")
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
                    coin = float(line[1][0])
                elif n == 2:
                    cash = float(line[1][0])
                else:
                    break
        print_help_text(self.device_id, "当前金币：%s 当前现金：%s" % (str(coin), str(cash)))
        return coin, cash

    # 看视频
    def watch_video(self, times=30):
        self.back_main_coin()
        tap(self.device_id, self.main_position)
        for i in range(times):
            print_help_text(self.device_id, "第%s/%s次刷视频" % (str(i + 1), str(times)))
            up_short_swipe(self.device_id)
            time.sleep(get_random_time(10, 15))

    # 返回首页再进入任务页面
    def back_main_coin(self):
        # 点击底部菜单金币按钮 最多10次
        for i in range(10):
            self.rm_ad()
            print_help_text(self.device_id, "回到首页")
            stats, positon = find_screen_text_button_position(self.device_id, "首页", "首页", top_normal_bottom="bottom")
            if stats:
                break
            else:
                press_back(self.device_id)
            if i > 4:
                self.shut_app()
                time.sleep(1)
                self.start_kuaishou_app()
                break

    # 上滑到最顶部
    def back_top(self):
        for i in range(3):
            down_long_swipe(self.device_id)

    # 看广告
    def ad(self):
        while True:
            print_help_text(self.device_id, "开始看广告")
            time.sleep(27)
            tap(self.device_id, self.ad_end)
            stats, position = find_screen_text_button_position(self.device_id, "去完成", "去完成")
            if stats:
                tap(self.device_id, position)
                time.sleep(1)
                tap(self.device_id, self.ad_end)
            stats, box, result = find_screen_text_position(self.device_id, "再看一")
            if stats:
                position =find_screen_by_result(result, "再看一")
                print_help_text(self.device_id, "再看一个")
                tap(self.device_id, position)
                continue
            position = find_screen_by_result(result, "继续观看")
            if position:
                print_help_text(self.device_id, "继续观看")
                tap(self.device_id, position)
                continue
            position = find_screen_by_result(result, "放弃")
            if position:
                print_help_text(self.device_id, "放弃任务")
                tap(self.device_id, position)
            break

    # 刷广告
    def watch_ad(self):
        # 先回到首页
        self.back_main_coin()
        # 点击去赚钱
        tap(self.device_id, self.task_position)
        self.rm_ad()
        self.back_top()
        for i in range(3):
            print_help_text(self.device_id, "找看广告按钮")
            stats, position = find_screen_text_button_position(self.device_id, "金币悬赏", "福利")
            if stats:
                print_help_text(self.device_id, "点击看广告")
                tap(self.device_id, position)
                self.ad()
                return True
            else:
                up_long_swipe(self.device_id)
        return False

    # 关掉广告
    def rm_ad(self):
        time.sleep(2)
        stats, box, result = find_screen_text_position(self.device_id, "看视频最高得")
        if stats:
            print_help_text(self.device_id, "在赚钱页面去掉广告！")
            # 点击查看视频
            print_help_text(self.device_id, "直接点击看广告")
            position = find_screen_by_result(result, "看视频最高")
            tap(self.device_id, position)
            self.ad()
            return True
        position = find_screen_by_result(result, "再看一")
        if position:
            print_help_text(self.device_id, "再看一个")
            tap(self.device_id, position)
            self.ad()
            return True
        position = find_screen_by_result(result, "看广告视频")
        if position:
            print_help_text(self.device_id, "点击看广告")
            tap(self.device_id, position)
            self.ad()
            return True
        position = find_screen_by_result(result, "继续观看")
        if position:
            print_help_text(self.device_id, "点击继续观看")
            tap(self.device_id, position)
            self.ad()
            return True

    # 刷宝箱
    def coin_box(self):
        # 刷宝箱
        self.back_main_coin()
        tap(self.device_id, self.task_position)
        self.rm_ad()
        status, position = find_screen_text_button_position(self.device_id, "开宝箱得金币", "开宝箱得金币")
        if status:
            print_help_text(self.device_id, "开宝箱")
            tap(self.device_id, position)
            time.sleep(1)
            # 点击看广告
            tap(self.device_id, self.coin_box_ad)
            self.ad()
        else:
            print_help_text(self.device_id, "当前无宝箱可看")

    def shopping(self):
        self.back_main_coin()
        # 点击红包菜单
        print_help_text(self.device_id, "点击去赚钱")
        tap(self.device_id, self.task_position)
        self.rm_ad()
        for i in range(4):
            stats, position = find_screen_text_button_position(self.device_id, "逛街领", "去逛街")
            if not stats:
                up_long_swipe(self.device_id)
                continue
            else:
                print_help_text(self.device_id, "点击去逛街")
                tap(self.device_id, position)
                for i in range(150):
                    print_help_text(self.device_id, "逛街第%s/200次" % str(i + 1))
                    up_short_swipe(self.device_id)
                    time.sleep(5)
                print_help_text(self.device_id, "返回")
                press_back(self.device_id)
                stats, position = find_screen_text_button_position(self.device_id, "放弃奖励", "放弃奖励")
                if stats:
                    tap(self.device_id, position)
                break

    def auto_run(self, light_screen_stats=False, watch_video=True, watch_coin_box=True, watch_ad=True, shopping=False):
        # 解锁手机
        if light_screen_stats:
            print_help_text(self.device_id, "解锁手机")
            unlock_device(self.device_id)
        # 打开抖音极速版
        print_help_text(self.device_id, "打开快手")
        self.start_kuaishou_app()
        time.sleep(1)
        # 获取当前收益
        coin_start, cash_start = self.get_coin_num()
        # 看广告
        if watch_ad:
            stats = True
            while stats:
                stats = self.watch_ad()
        # 看宝箱
        if watch_coin_box:
            print_help_text(self.device_id, "刷宝箱")
            self.coin_box()
        # 看10分钟视频
        if watch_video:
            print_help_text(self.device_id, "开始看视频")
            self.watch_video()
        # 逛街
        if shopping:
            print_help_text(self.device_id, "去逛街")
            self.shopping()
        # 获取当前收益
        coin_end, cash_end = self.get_coin_num()
        self.coin_current = coin_end - coin_start
        self.cash_current = round(self.coin_current / 10000, 4)
        self.coin_today = coin_end
        self.cash_total = cash_end


if __name__ == "__main__":
    ks_obj = KuaiShouOpt("192.168.31.227:5555")
    # ks_obj.auto_run(light_screen_stats=False, watch_video=False, watch_ad=False, watch_coin_box=True, shopping=True)
    # print(ks_obj.get_coin_num())
    ks_obj.shopping()