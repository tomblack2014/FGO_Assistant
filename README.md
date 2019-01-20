运行main.py即可执行
新建policy文件夹，新建battle_policy.json文件来设置关卡策略
battle_policy.json文件格式如下：
{
    "task_type": "cloth",   # cloth表示优先找礼装， servant表示优先找从者
    "AP_supply": 1, # 1 ,2 ,3 表示优先吃金，银，铜果子
    "policy":
    {
        "turn_1":  # turn_n表示第n回合的策略
        {
            "skill_list": ["skill3_1"] # 放技能的顺序，skilla_b表示a从者的b技能，按list中的顺序释放
        },
        "turn_3":
        {
            "skill_list": ["skill2_2", "skill2_3"],
            "weapon":[2] # 放第二个从者宝具
        },
        "turn_4":
        {
            "skill_list": ["skill1_1", "open_master_skill", "mskill2", "skill_left_servant", "skill3_2"],
            "weapon":[1]
        }

    }

}

