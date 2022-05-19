from article_lite import *
from ugc_lite import *

if __name__ == "__main__":
    # 如果没有设备 则重启adb 服务
    if len(CurrentDeviceList) == 0:
        print("重启adb服务")
        reboot_adb()
    else:
        print("本次连接设备：")
        [print(i) for i in CurrentDeviceList]

    # ************************** 今日头条 **************************
    # 今日头条极速版刷金币 可以10分钟刷一次 广告一共10次 逛商场一共10次 开宝箱没限制
    article_lite_opt = ArticleLiteOpt()
    ugc_lite_obj = UGCLiteOpt()

    first_status = False
    if first_status:
        article_lite_opt.auto_run(light_screen_stats=True, read_article=True, watch_small_video=True,
                                           watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run()
    else:
        article_lite_opt.auto_run(light_screen_stats=False, read_article=False, watch_small_video=False,
                                           watch_coin_box=True, watch_ad=True, watch_goods=True)
        ugc_lite_obj.auto_run(watch_video=False, watch_baokuan=False)