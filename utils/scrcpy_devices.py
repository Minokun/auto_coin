import subprocess, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.phone_opt import CurrentDeviceList

os.environ["PATH"] = 'C:/Program Files (x86)/scrcpy-win64-v1.24/' + os.pathsep + os.getenv("PATH")

def scrcpy_command(device):
    window_title = device.split(':')[0]
    command = 'scrcpy.exe -s %s -b 2M -m 1024 --window-title %s' % (device, window_title)
    print(command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    result = p.communicate()[0].decode()
    return result.split('\r\n')

def run_scrcpy():
    max_workers = len(CurrentDeviceList)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    all_task = []
    for i in CurrentDeviceList:
        executor.submit(scrcpy_command, i)
    for future in as_completed(all_task):
        data = future.result()
        print(data)

if __name__ == "__main__":
    run_scrcpy()