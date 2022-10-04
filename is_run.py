# 使用psutil来判断
import psutil


def proc_exist(process_name):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == process_name:
            return pid


# if isinstance(proc_exist('chrome.exe'), int):
#     print('chrome.exe is running')
# else:
#     print('no such process...')
