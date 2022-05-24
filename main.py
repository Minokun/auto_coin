import math
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from phone_opt import CurrentDeviceList, unclock_all_devices, print_help_text, unlock_device
from article_lite import ArticleLiteOpt
from ugc_lite import UGCLiteOpt
from ugc import UGCOpt
from dragon_read import DragonReadOpt

total_num = 30
total_end_num = 0


def run(device_id, first_status=False):
    global total_end_num, total_num
    start_time = datetime.now()
    print_help_text(device_id, "启动程序!")
    if first_status:
        unlock_device(device_id)
    # 今日头条极速版
    article_lite_opt = ArticleLiteOpt(device_id)
    # 抖音极速版
    ugc_lite_obj = UGCLiteOpt(device_id)
    # 抖音
    ugc_obj = UGCOpt(device_id)
    # 番茄小说
    dragon_read = DragonReadOpt(device_id)
    if first_status:
        # 每天第一次运行 需要做活跃和只有一次的任务
        article_lite_opt.auto_run(first_status=first_status, light_screen_stats=False, read_article=True, watch_small_video=True,
                                  watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run(light_screen_stats=False, watch_video=False, watch_coin_box=False)
        ugc_obj.auto_run(light_screen_stats=False)
        dragon_read.auto_run(light_screen_stats=False)
    else:
        article_lite_opt.auto_run(first_status=first_status, light_screen_stats=False, read_article=False, watch_small_video=False,
                                  watch_coin_box=True, watch_ad=True, watch_goods=False)
        ugc_lite_obj.auto_run(light_screen_stats=False, watch_video=False, watch_baokuan=False, watch_coin_box=True,
                              watch_ad=True, shopping=False)
        ugc_obj.auto_run(light_screen_stats=False, watch_video=False)
        dragon_read.auto_run(light_screen_stats=False)
    total_end_num += 1
    end_time = datetime.now()
    run_time = (end_time - start_time).seconds
    run_time_minutes = math.ceil(run_time / 60)
    run_time_rest_seconds = run_time % 60
    runtime_text = str(run_time_minutes) + "分" + str(run_time_rest_seconds) + "秒"
    return "\r\n设备：%s 第%s/%s次 运行结束 开始时间：%s 结束时间：%s 耗时:%s" % (device_id, total_end_num, total_num, start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S"), runtime_text)


def main():
    # 解锁所有设备
    unclock_all_devices()
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    all_task = []
    first_status = False
    for n in range(1, total_num + 1):
        for i in CurrentDeviceList:
            if first_status and n == 1:
                all_task.append(
                    executor.submit(run, *(i, True))
                )
            else:
                all_task.append(
                    executor.submit(run, *(i, False))
                )
    for future in as_completed(all_task):
        data = future.result()
        print(data)


if __name__ == "__main__":
    main()
