import subprocess, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.phone_opt import CurrentDeviceList
import win32gui, win32api, win32con

os.environ["PATH"] = 'C:/Program Files (x86)/scrcpy-win64-v1.24/' + os.pathsep + os.getenv("PATH")
os.environ["PATH"] = 'C:/scrcpy-win64-v1.24' + os.pathsep + os.getenv("PATH")
window_x = 100
window_y = 50

def window_controller(device):
    global window_x, window_y
    print(window_x, window_y)
    time.sleep(1)
    window_name = device.split(':')[0]
    handle = win32gui.FindWindow(None, window_name)
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    win32gui.SetForegroundWindow(handle)
    move_x = left + 10
    move_y = top + 10
    win32api.SetCursorPos((move_x, move_y))  # 鼠标挪到窗口所在坐标
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # 鼠标左键按下
    win32api.SetCursorPos((window_x, window_y))  # 鼠标左键按下的同时移动鼠标位置，实现拖动框体，这里是要移动到左上角，但是不能写（0,0），（0,0）+（x偏移值，y偏移值），确保框体的左上角在窗口的左上角
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)  # 鼠标左键抬起
    # pos = win32api.GetCursorPos()
    window_x = window_x + right - left - 15

def scrcpy_command(device, time_period):
    window_title = device.split(':')[0]
    command = 'scrcpy.exe -s %s -b 2M -m 720 --window-title %s' % (device, window_title)
    print(command)
    # time.sleep(time_period)
    os.system(command)

def run_scrcpy():
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    all_task = []
    n = 1
    for i in CurrentDeviceList:
        n += 1
        executor.submit(scrcpy_command, *(i, n))
        time.sleep(1.5)
        window_controller(i)
    for future in as_completed(all_task):
        data = future.result()
        print(data)

if __name__ == "__main__":
    run_scrcpy()