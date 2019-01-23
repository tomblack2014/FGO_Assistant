import pyautogui as pg
import time
import cv2
import aircv as ac

buster_color = [247, 0, 0]
arts_color = [8, 99, 254]
quick_color = [249, 255, 166]

def click_wait(pos, t):
    """点击某一位置并等待t秒"""
    pg.click(pos)
    time.sleep(t)

def locateonRegion(image, region=None):
    """在区域region内查找图image"""
    try:
        screenshotIm = pg.screenshot(
            region=region)
        retVal = pg.locate(image, screenshotIm)
        return retVal
    except Exception:
        return None


def find_color(region, color, sim=0):
    screen = pg.screenshot()
    for i in range(region[0], region[2]):
        for j in range(region[1], region[3]):
            pixel_r, pixel_g, pixel_b = screen.getpixel((i, j))
            dist = abs(color[0] - pixel_r) + abs(color[1] - pixel_g) + abs(color[2] - pixel_b)
            if dist <= sim:
                return [i, j]
    return None

def check_over(t, dict):
    s = time.time()
    e = time.time()
    while e - s < t:
        res_pos = find_color(dict["result_region"], dict["result_color"])
        if res_pos:
            return True
        e = time.time()
    return False

class PosConverter:
    def SetBasePos(self, leftTop, rightBottom):
        self.leftTop = leftTop
        self.rightBottom = rightBottom

    def GetPos(self, src):
      dst = [0, 0]
      for i in range(0, 2):
          dst[i] = self.leftTop[i] + (self.rightBottom[i] - self.leftTop[i]) * src[i]
      return dst

def FindOnScreen(img, th=0.7):
    imobj = ac.imread(img)
    screen = pg.screenshot()
    screen.save("img/screen.png")
    imsrc = ac.imread("img/screen.png")
    pos = ac.find_template(imsrc, imobj)
    if pos:
        if (pos['confidence'] > th):
            return pos['result']

class Card:
    def __init__(self, name, color, pos):
        self.name = name
        self.color = color
        self.pos = pos


def get_cards(points_dict):
    # 扫描指令卡
    color_num = [0, 0, 0]
    cards = []
    for i in range(0, 5):
        region = points_dict['ordercards_region'][i*2] + points_dict['ordercards_region'][i*2 + 1]
        region = [round(num) for num in region]
        card_pos = points_dict['ordercards_center'][i]
        buster_pos = find_color(region, buster_color, 5)
        art_pos = find_color(region, arts_color, 5)
        quick_pos = find_color(region, quick_color, 5)
        for j, now_pos in enumerate([buster_pos, art_pos, quick_pos]):
            if now_pos:
                card_color = j
                color_num[card_color] += 1
                break
            if j == 2:
                card_color = j
                color_num[card_color] += 1
        now_card = Card('', card_color, card_pos)
        cards.append(now_card)
    return cards, color_num

if __name__ == '__main__':
    while True:
        choice = input("输入指令，1:鼠标取位置， 2:找图所有出现的位置, 3:退出")
        print("2s后开始执行，请切到模拟器")
        for i in range(2, 0, -1):
            print("{} s".format(i))
            time.sleep(1)
        if choice == "1":
            print(pg.position())


        elif choice == "2":
            img_pos = pg.locateOnScreen('img/huaban1.png')
            if img_pos:
                print(img_pos)
                pg.moveTo(img_pos[0], img_pos[1])
                time.sleep(1)
        elif choice == '3':
            region = [0, 0, 1000, 1000]
            img_pos = locateonRegion('test.png', region)
            if img_pos:
                print(img_pos)
        elif choice == '4':
            region = [995, 187, 1000, 221]
            r, g, b = 246, 250, 250
            pos = find_color(region, [r, g, b])
            if pos:
                pg.moveTo(pos)
        else:
            break
