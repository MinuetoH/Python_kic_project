# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:04:10 2022

@author: kimyh
"""

import dlib
import cv2
import numpy as np

def imgSticker(img_orig, img_sticker, detector_hog, landmark_predictor):
    img_rgb = cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB)
    dlib_rects = detector_hog(img_rgb, 0)
    if len(dlib_rects) < 1:
        return img_orig

    list_landmarks = []
    for dlib_rect in dlib_rects:
        points = landmark_predictor(img_rgb, dlib_rect)
        list_points = list(map(lambda p: (p.x, p.y), points.parts()))
        list_landmarks.append(list_points)

    # for dlib_rect, landmark in zip(dlib_rects, list_landmarks):
    #     x = landmark[30][0]
    #     y = landmark[30][1] - dlib_rect.width()//2
    #     w = dlib_rect.width()
    #     h = dlib_rect.width()
    #     break

    # for dlib_rect, landmark in zip(dlib_rects, list_landmarks):
    #     print("lips index:", landmark[62])  # lips index
    #     Px = landmark[20][0]
    #     Py = landmark[62][1]
    #     w = h = dlib_rect.width()
    #     # position of nose
    #     # print('(x,y) : (%d,%d)' % (x, y))
    #     # pic rate
    #     print('(w,h) : (%d,%d)' % (w, h))
    #     # lips index: (1209, 2325)
    #     # (x, y): (1209, 2900)
    #     # (w, h): (1151, 1151)

    for dlib_rect, landmark in zip(dlib_rects, list_landmarks):
        x1 = landmark[2][0]
        y1 = landmark[2][1]
        x2 = landmark[30][0]
        y2 = landmark[30][1]
        x3 = landmark[36][0]
        y3 = landmark[36][1]
        x4 = landmark[48][0]
        y4 = landmark[48][1]

        x5 = landmark[14][0]
        y5 = landmark[2][1]
        x6 = landmark[30][0]
        y6 = landmark[30][1]
        x7 = landmark[45][0]
        y7 = landmark[36][1]
        x8 = landmark[54][0]
        y8 = landmark[48][1]

        # 4좌표가 주어질때 교점 구하기 : https://gaussian37.github.io/math-algorithm-intersection_point/

        Px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) // (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        Py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) // (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        cv2.circle(img_rgb, (Px, Py), 5, (0, 0, 255), -1)

        Px2 = ((x5 * y6 - y5 * x6) * (x7 - x8) - (x5 - x6) * (x7 * y8 - y7 * x8)) // (
                (x5 - x6) * (y7 - y8) - (y5 - y6) * (x7 - x8))
        Py2 = ((x5 * y6 - y5 * x6) * (y7 - y8) - (y5 - y6) * (x7 * y8 - y7 * x8)) // (
                (x5 - x6) * (y7 - y8) - (y5 - y6) * (x7 - x8))
        cv2.circle(img_rgb, (Px2, Py2), 5, (0, 0, 255), -1)

        w = Px2 - Px
        h = Px2 - Px

        print('(w,h) : (%d,%d)' % (w, h))

    # sticker
    img_sticker = cv2.resize(img_sticker, (w, h), interpolation=cv2.INTER_NEAREST)

    refined_x = Px  # left
    refined_y = Py - img_sticker.shape[0] // 2  # top

    print('(x,y) : (%d,%d)' % (refined_x, refined_y))

    if refined_y < 0:
        img_sticker = img_sticker[-refined_y:]
        refined_y = 0

    img_bgr = img_orig.copy()
    sticker_area = img_bgr[refined_y:refined_y + img_sticker.shape[0], refined_x:refined_x + img_sticker.shape[1]]

    img_bgr[refined_y:refined_y + img_sticker.shape[0], refined_x:refined_x + img_sticker.shape[1]] = \
        np.where(img_sticker == 255, sticker_area, img_sticker).astype(np.uint8)

    return img_bgr


detector_hog = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor\
    ('./model/shape_predictor_68_face_landmarks.dat')

vc = cv2.VideoCapture('./images/vedeo2.MP4')
img_sticker = cv2.imread('images/mouth1.jpg')

vlen = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

# writer 초기화
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vw = cv2.VideoWriter('./images/output.mp4', fourcc, 30, (1280, 720))

for i in range(vlen):
    ret, img = vc.read()
    if ret == False:
        break

    start = cv2.getTickCount()
    img_result = imgSticker\
        (img, img_sticker.copy(), detector_hog, landmark_predictor)
    time = (cv2.getTickCount() - start) / cv2.getTickFrequency() * 1000
    print('[INFO] time: %.2fms' % time)

    # 매 프레임 마다 저장합니다.
    vw.write(cv2.resize(img_result, (1280, 720)))

    cv2.imshow('show', img_result)
    key = cv2.waitKey(1)
    if key == 27:
        break

vw.release()
cv2.destroyAllWindows()
