from typing import List
import numpy as np
import cv2


def check_rect_contain_point(rects, coordinates):
    new_array = []

    if len(rects) <= 0 or len(coordinates) <= 0:
        return new_array
    for rect in rects:
        flag = False
        for coordinate in coordinates:
            if coordinate[1] >= rect[0] and coordinate[1] <= rect[2] and coordinate[0] >= rect[1] and coordinate[0] <= rect[3]:
                flag = True
                break
        if flag:
            new_array.append(rect)
    return new_array

def checkOverlap(boxa, boxb):
    ax1, ay1, ax2, ay2 = boxa
    bx1, by1, bx2, by2 = boxb
    if (ax1 > bx2):
        return 0
    if (ay1 > by2):
        return 0
    if (ax2 < bx1):
        return 0
    if (ay2 < by1):
        return 0
    if (ax2 == bx1 or ay2 == by1):
        return 1
    colInt = abs(min(ax2, bx2) - max(ax1, bx1))
    rowInt = abs(min(ay2, by2) - max(ay1, by1))
    overlap_area = colInt * rowInt
    area1 = (ax2 - ax1) * (ay2 - ay1)
    area2 = (bx2 - bx1) * (by2 - by1)
    return overlap_area / (area1 + area2 - overlap_area)

def unionBox(a, b):
    x1 = min(a[0], b[0])
    y1 = min(a[1], b[1])
    x2 = max(a[2], b[2])
    y2 = max(a[3], b[3])
    return [x1, y1, x2, y2]


def rectMerge_sxf(rects: List):
    # rects => [[x1, y1, w1, h2], [x2, y2, w2, h3], ...]
    '''
    当通过connectedComponentsWithStats找到rects坐标时，
    注意前2個坐标是表示整個圖的，需要去除，不然就只有一個大框，
    在执行此函数前，可执行类似下面的操作。
    rectList = sorted(rectList)[2:]
    '''
    rectList = rects.copy()
    rectList.sort()
    new_array = []
    complete = 1
    # 要用while，不能forEach，因爲rectList內容會變
    i = 0
    while i < len(rectList):
        # 選後面的即可，前面的已經判斷過了，不需要重復操作
        j = i + 1
        succees_once = 0
        while j < len(rectList):
            boxa = rectList[i]
            boxb = rectList[j]
            # 判斷是否有重疊，注意只針對水平＋垂直情況，有角度旋轉的不行
            if checkOverlap(boxa, boxb):
                complete = 0
                # 將合並後的矩陣加入候選區
                new_array.append(unionBox(boxa, boxb))
                succees_once = 1
                # 從原列表中刪除，因爲這兩個已經合並了，不刪除會導致重復計算
                rectList.remove(boxa)
                rectList.remove(boxb)
                break
            j += 1
        if succees_once:
            # 成功合並了一次，此時i不需要+1，因爲上面進行了remove(boxb)操作
            continue
        i += 1
    # 剩餘項是不重疊的，直接加進來即可
    new_array.extend(rectList)

    # 0: 可能還有未合並的，遞歸調用;
    # 1: 本次沒有合並項，說明全部是分開的，可以結束退出
    if complete == 0:
        complete, new_array = rectMerge_sxf(new_array)
    return complete, new_array