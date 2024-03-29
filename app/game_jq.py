import time
import re
import cv2
import numpy as np
from utils.phone_opt import *
from concurrent.futures import ThreadPoolExecutor

class JQ():
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "JQ"
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        self.buy_button = (550, int(2180 * self.height_scale))
        self.ad_shut = (1000, int(230 * self.height_scale))

    def ad(self):
        time.sleep(38)
        print_help_text(self.device_id, "关闭广告")
        self.ad_shut = find_ad_shut(self.device_id)
        tap(self.device_id, self.ad_shut)
        self.ad_shut = find_ad_shut(self.device_id)
        if self.ad_shut[1] > 50 and self.ad_shut[1] < 250:
            tap(self.device_id, self.ad_shut)
        stats, position = find_screen_text_button_position(self.device_id, "开心收下", "开心收下")
        if stats:
            tap(self.device_id, position)

    def auto_combine_button(self):
        stats, box, result = find_screen_text_position(self.device_id, "停止合成")
        if stats:
            return True
        position = find_screen_by_result(result, "自动合成")
        if position:
            print_help_text(self.device_id, "点击自动合成")
            tap(self.device_id, position)
            time.sleep(1)
            stats, position = find_screen_text_button_position(self.device_id, "看视频开启", "看视频开启")
            if stats:
                tap(self.device_id, position)
            self.ad()
        time.sleep(1)

    def zp(self):
        stats, position = find_screen_text_button_position(self.device_id, "转盘", "转盘")
        if stats:
            tap(self.device_id, position)
            while True:
                stats, box, result = find_screen_text_position(self.device_id, "立刻抽奖")
                if stats:
                    position = find_screen_by_result(result, '立刻抽奖')
                    if position:
                        print_help_text(self.device_id, "立即抽奖")
                        tap(self.device_id, position)
                        time.sleep(2)
                        stats, box, result = find_screen_text_position(self.device_id, "开心收下")
                        if stats:
                            print_help_text(self.device_id, "开心收下")
                            position = find_screen_by_result(result, "开心收下")
                            tap(self.device_id, position)
                            continue
                        position = find_screen_by_result(result, "领取")
                        if position:
                            print_help_text(self.device_id, "看广告")
                            tap(self.device_id, position)
                            self.ad()
                            continue
                    position = find_screen_by_result(result, "恢复")
                    if position:
                        print_help_text(self.device_id, "恢复")
                        tap(self.device_id, position)
                        self.ad()
                        continue
                position = find_screen_by_result(result, "恢复次数")
                if position:
                    tap(self.device_id, position)
                    self.ad()
                    continue
                break
            press_back(self.device_id)

    def main(self):
        self.zp()
        while True:
            self.auto_combine_button()
            print_help_text(self.device_id, "自动购买建筑")
            stats, box, result = find_screen_text_position(self.device_id, "立即领取")
            if stats:
                position = find_screen_by_result(result, "立即领取")
                tap(self.device_id, position)
                self.ad()
            position = find_screen_by_result(result, "暂无")
            if position:
                print_help_text(self.device_id, "当前金币领取完毕")
                break
            for i in range(10):
                tap(self.device_id, self.buy_button)

def main():
    # 解锁所有设备
    # unclock_all_devices()
    # CurrentDeviceList = ['192.168.101.103:5555']
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    for i in CurrentDeviceList:
        jq_obj = JQ(i)
        # jq_obj.main()
        executor.submit(jq_obj.main)

def click(device_id):
    while True:
        tap(device_id, (530, 2250), sleep_time=0.3)

def find_ad_shut(device_id):
    png_name, local_png = get_img(device_id)
    img_path = local_png
    temple_path = '../media/template.png'
    img = cv2.imread(img_path)
    img[np.where((img == [255, 255, 255]).all(axis=2))] = [0, 0, 0]
    temple = cv2.imread(temple_path)
    result = cv2.matchTemplate(img, temple, cv2.TM_SQDIFF_NORMED)
    # 返回匹配的最小坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    tl = min_loc
    br = (int(tl[0]) + 20, int(tl[1]) + 20)
    print(br)
    return br

def test():
    import numpy as np
    img_path = '../media/101.png'
    temple_path = '../media/template.png'
    img = cv2.imread(img_path)
    temple = cv2.imread(temple_path)
    # 获取到小图的尺寸
    th, tw = temple.shape[:2]
    result = cv2.matchTemplate(img, temple, cv2.TM_SQDIFF_NORMED)
    # 返回匹配的最小坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, max_val, min_loc, max_loc)
    tl = min_loc
    print(tl)
    br = (int(tl[0]) + tw, int(tl[1]) + th)
    print('br==', br)
    cv2.rectangle(img, tl, br, [0, 255, 0])
    cv2.imshow("匹配结果" + np.str(cv2.TM_SQDIFF_NORMED), img)
    if cv2.waitKey() == 'q':
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    # click(device_id='192.168.31.213:5555')
    # test()