import win32gui, win32api, win32con
import time
x = 100
y = 50
time.sleep(1)
for i in ('192.168.101.101', '192.168.101.103', '192.168.101.104'):
    handle = win32gui.FindWindow(None, i)
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    win32gui.SetForegroundWindow(handle)
    move_x = left + 10
    move_y = top + 10
    win32api.SetCursorPos((move_x, move_y))  # 鼠标挪到窗口所在坐标
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)  # 鼠标左键按下
    win32api.SetCursorPos((x, y))  # 鼠标左键按下的同时移动鼠标位置，实现拖动框体，这里是要移动到左上角，但是不能写（0,0），（0,0）+（x偏移值，y偏移值），确保框体的左上角在窗口的左上角
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)  # 鼠标左键抬起
    # pos = win32api.GetCursorPos()
    x = x + right - left - 15