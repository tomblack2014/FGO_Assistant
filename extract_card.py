from PIL import ImageGrab
import pyautogui as pg
#from win32api import GetSystemMetrics
import time
import json
from basic_op import *

if __name__ == '__main__':
    start = input("输入1后开始，否则退出")
    if start == '1':
        print("5s后开始执行，请切到模拟器")
        for i in range(5, 0, -1):
            print("{} s".format(i))
            time.sleep(1)
        print("开始执行")
        points_dict = json.load(open("points.json", 'r', encoding='utf-8'))
        times = 1
        while True:
            reset_pos = FindOnScreen('img/reset_bonus.png', 0.9)
            if reset_pos:
                click_wait(reset_pos, 1)
                times += 1
                click_wait([1149, 749], 3)
                click_wait([933, 751], 1)

                if times > 108:
                    break
            for _ in range(10):
                click_wait([694, 616], 0.5)
