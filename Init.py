import json
from basic_op import *

def Init():
    points_dict = json.load(open("points.json", 'r', encoding='utf-8'))
    leftTop = points_dict['left_top']
    rightBottom = points_dict['right_bottom']
    points_dict.pop('left_top')
    points_dict.pop('right_bottom')

    converter = PosConverter()
    converter.SetBasePos(leftTop, rightBottom)

    for key in points_dict:
        if len(points_dict[key]) > 2:
            for i in range(0, len(points_dict[key])):
                points_dict[key][i] = converter.GetPos(points_dict[key][i])
        else:
            points_dict[key] = converter.GetPos(points_dict[key])

    zhijie1 = points_dict['class_choose1']
    zhijie9 = points_dict['class_choose9']
    dist = (zhijie9[0] - zhijie1[0]) / 8
    zhijie = [[zhijie1[0] + dist * i, zhijie1[1]] for i in range(0, 9)]
    points_dict.pop('class_choose1')
    points_dict.pop('class_choose9')
    points_dict['class_choose'] = zhijie

    return points_dict
