import json
from basic_op import *
from Init import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FGO_Assistant')
    parser.add_argument('--policy',
                        default="policy/battle_policy.json",
                        help='Path to a policy file')

    args = parser.parse_args()

    pos_dict = Init()
    pg.FAILSAGE = False
    start = input("输入1后开始，否则退出")
    if start == '1':
        print("5s后开始执行，请切到模拟器")
        for i in range(4, 0, -1):
            print("{} s".format(i))
            time.sleep(1)
        print("开始执行")
        policy = json.load(open(args.policy, 'r', encoding='utf-8'))
        PassTimes = 0

        # 主循环
        while True:

            # 判断是否在开始界面
            while True:
                start_pos = FindOnScreen('img/menu.png')
                if start_pos:
                    break
                # 判断是否卡在上一场战斗结束添加好友界面
                noadd = pg.locateOnScreen('img/noadd.png')
                if noadd:
                    click_wait(noadd, 1)
                time.sleep(1)
            # 寻找关卡
            while True:
                target = FindOnScreen('img/targetTask.png')
                if target:
                    click_wait(target, 1)
                    break
                time.sleep(1)

            # 判断是否需要嗑果子
            # TODO:判断吃所有果子的逻辑
            apple_pos = FindOnScreen('img/golden_apple.png')
            if apple_pos:
                click_wait(apple_pos, 1)
                click_wait(pos_dict['AP_ok_btn'], 3)

            # 找礼装
            # TODO：增加阶职定向翻页查找功能
            find = 0
            freshTimes = 0
            while find == 0:
                task_pos = None
                if policy['task_type'] == 'cloth':
                    task_pos = FindOnScreen('img/targetClothes.png')
                    if task_pos:
                        click_wait([task_pos[0], task_pos[1]], 2)
                        find = 1
                        break
                else:
                    task_pos = FindOnScreen('img/targetServant.png')
                    if task_pos:
                        click_wait([task_pos[0], task_pos[1]], 2)
                        find = 1
                        break
                if find == 0:
                    click_wait(pos_dict['update_list'], 1)
                    click_wait(pos_dict['update_yes'], 10)
                    freshTimes += 1
                time.sleep(1)
            print("本次找礼装刷新{}次".format(freshTimes))

            # 点击开始任务
            click_wait(pos_dict['start_btn'], 1)
            print("开始新的一次关卡")
            # 一直打到结束
            turn = 0
            over = 0

            while True:
                atk_btn = 0
                # 等到加载完成，出现attack_btn或者result
                while True:
                    atk_btn = FindOnScreen('img/atk_btn.png')
                    if atk_btn:
                        break
                    result = FindOnScreen('img/result.png')
                    if result:
                        print("result")
                        over = 1
                        break
                    time.sleep(1)
                if over == 1:
                    break
                turn += 1

                # 不同回合的技能开启
                # TODO:用配置文件控制
                print("回合{}:释放技能".format(turn))
                t_str = "turn_" + str(turn)
                turn_policy = policy['policy']
                if t_str in turn_policy:
                    if "skill_list" in turn_policy[t_str]:
                        skill_lists = turn_policy[t_str]['skill_list']
                        for skill in skill_lists:
                            if skill.startswith('wait'):
                                time.sleep(5)
                            else:
                                if skill.startswith('skill'):
                                    click_wait(pos_dict[skill], 3)
                                else:
                                    click_wait(pos_dict[skill], 0.5)
                            

                click_wait(atk_btn, 2.5)
                # 释放宝具
                # TODO：配置文件
                if t_str in turn_policy:
                    if "weapon" in turn_policy[t_str]:
                        weapon_list = turn_policy[t_str]['weapon']
                        for weapon in weapon_list:
                            weapon_pos = "baoju" + str(weapon)
                            click_wait(pos_dict[weapon_pos], 0.3)

                # 扫描卡牌，计算各色数量
                # TODO：有空这块逻辑可以好好优化改进一下，为了跑通暂时五张卡从左到右出
                for i in range(0, 5):
                    click_wait(pos_dict['ordercards_center'][i], 0.3)
                time.sleep(15)
            # 结束结算页面
            PassTimes += 1
            print("通关,当前第{}次".format(PassTimes))
            click_wait(pos_dict['class_choose'][0], 2)
            click_wait(pos_dict['class_choose'][0], 2)
            click_wait(pos_dict['class_choose'][0], 2)
            click_wait(pos_dict['next_btn'], 1)
