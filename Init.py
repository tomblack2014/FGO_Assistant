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
        if type(points_dict[key][0]).__name__ != "float":
            for i in range(0, len(points_dict[key])):
                points_dict[key][i] = converter.GetPos(points_dict[key][i])
        else:
            points_dict[key] = converter.GetPos(points_dict[key])
    class1 = points_dict['class_choose1']
    class9 = points_dict['class_choose9']
    dist = (class9[0] - class1[0]) / 8
    classes = [[class1[0] + dist * i, class1[1]] for i in range(0, 9)]
    points_dict.pop('class_choose1')
    points_dict.pop('class_choose9')
    points_dict['class_choose'] = classes

    return points_dict
