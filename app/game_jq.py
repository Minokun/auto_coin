import time
import re
from utils.phone_opt import *
from concurrent.futures import ThreadPoolExecutor

class JQ():
    def __init__(self, device_id):
        self.device_id = device_id
        self.app_name = "JQ"
        self.wight, self.height = get_phone_wh(self.device_id)
        self.height_scale = int(self.height) / 2400
        self.buy_button = (550, int(2300 * self.height_scale))
        self.ad_shut = (1000, int(230 * self.height_scale))

    def ad(self):
        time.sleep(30)
        print_help_text(self.device_id, "关闭广告")
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

    def main(self):
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
            position = find_screen_by_result(result, "购买建筑")
            if position:
                self.buy_button = position
            for i in range(8):
                tap(self.device_id, self.buy_button)

def main():
    # 解锁所有设备
    # unclock_all_devices()
    # CurrentDeviceList = ['192.168.101.101:5555']
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    for i in CurrentDeviceList:
        jq_obj = JQ(i)
        # jq_obj.main()
        executor.submit(jq_obj.main)

if __name__ == "__main__":
    main()