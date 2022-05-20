from phone_opt import CurrentDeviceList
from article_lite import ArticleLiteOpt
from ugc_lite import UGCLiteOpt
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from phone_opt import print_help_text

total_num = 30
total_end_num = 0


def run(device_id, first_status=False):
    global total_end_num, total_num
    print_help_text(device_id, "启动程序!")
    article_lite_opt = ArticleLiteOpt(device_id)
    ugc_lite_obj = UGCLiteOpt(device_id)
    if first_status:
        article_lite_opt.auto_run(light_screen_stats=True, read_article=True, watch_small_video=True,
                                           watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run(light_screen_stats=False)
    else:
        article_lite_opt.auto_run(light_screen_stats=True, read_article=False, watch_small_video=False,
                                           watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run(light_screen_stats=False, watch_video=False, watch_baokuan=False)
    total_end_num += 1
    return "设备：%s 第%s/%s次 运行结束" % (device_id, total_end_num, total_num)


def main():
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    all_task = []
    for i in CurrentDeviceList:
        for _ in range(total_num):
            all_task.append(
                executor.submit(run, *(i, False))
            )
    for future in as_completed(all_task):
        data = future.result()
        print(data)


if __name__ == "__main__":
    main()