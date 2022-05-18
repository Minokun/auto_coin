
# -*- coding:utf-8 -*-

import math
from phone_opt import *
from paddle_opt import *


# 抖音极速版
class UGCLiteOpt:
    def __init__(self):
        self.device_id_list = get_all_device_id()
        self.paddle_detect = DetectPic()
        self.app_name = "ugc_lite"
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

    def start_ugc_app(self):
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


if __name__ == "__main__":
    ugc_lite_obj = UGCLiteOpt()
    ugc_lite_obj.start_ugc_app()