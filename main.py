from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from phone_opt import CurrentDeviceList, unclock_all_devices, print_help_text, unlock_device
from article_lite import ArticleLiteOpt
from ugc_lite import UGCLiteOpt
from dragon_read import DragonReadOpt

total_num = 30
total_end_num = 0


def run(device_id, first_status=False):
    global total_end_num, total_num
    print_help_text(device_id, "启动程序!")
    if first_status:
        unlock_device(device_id)
    # 今日头条极速版
    article_lite_opt = ArticleLiteOpt(device_id)
    # 抖音极速版
    ugc_lite_obj = UGCLiteOpt(device_id)
    # 番茄小说
    dragon_read = DragonReadOpt(device_id)
    if first_status:
        # 每天第一次运行 需要做活跃和只有一次的任务
        article_lite_opt.auto_run(first_status=True, light_screen_stats=True, read_article=True, watch_small_video=True,
                                  watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run(light_screen_stats=False)
        dragon_read.auto_run(light_screen_stats=False)
    else:
        article_lite_opt.auto_run(first_status=False, light_screen_stats=False, read_article=True, watch_small_video=False,
                                  watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run(light_screen_stats=False, watch_video=False, watch_baokuan=False, watch_coin_box=True,
                              watch_ad=True, shopping=True)
        dragon_read.auto_run(light_screen_stats=False)
    total_end_num += 1
    return "设备：%s 第%s/%s次 运行结束" % (device_id, total_end_num, total_num)


def main():
    # 解锁所有设备
    unclock_all_devices()
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    all_task = []
    first_status = False
    for n in range(1, total_num + 1):
        for i in CurrentDeviceList:
            if first_status:
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
