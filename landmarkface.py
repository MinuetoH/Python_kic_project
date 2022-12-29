# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:04:10 2022

@author: kimyh
"""

import dlib
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier("./model/haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor\
    ('./model/shape_predictor_68_face_landmarks.dat')
    
# 얼굴의 각 구역의 포인트들을 구분
JAWLINE_POINTS = list(range(0,17))
RIGHT_EYEBROW_POINTS = list(range(17,22))
LEFT_EYEBROW_POINTS = list(range(22,27))
NOSE_POINTS = list(range(27,36))
RIGHT_EYE_POINTS = list(range(36,42))
LEFT_EYE_POINTS = list(range(42,48))
MOUTH_OUTLINE_POINTS = list(range(48,61))
MOUTH_INLINE_POINTS = list(range(61,68))

'''
    def = dlib을 이용해 얼굴과 눈을 찾는 함수
    input = gray 스케일 이미지
    output = 얼굴 중요 포인트 68개 점 + 이미지
'''

def detect(gray,frame) :
    faces = faceCascade.detectMultiScale\
        (gray, scaleFactor=1.05, minNeighbors=5, minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)
    
    #얼굴에서 랜드마크 찾기
    for (x, y, w, h) in faces :
        #오픈 cv 이미지를 dlib용 사각형으로 변환
        dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
        #랜드마크 포인트를 지정
        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, dlib_rect).parts()])
        #원하는 포인트를 넣는다 (전부)
        landmarks_display = landmarks[0:68]
        #눈만
        #landmarks_display = landmarks[RIGHT_EYE_POINTS, LEFT_EYE_POINTS]
        
        #포인트 출력
        for idx, point in enumerate(landmarks_display) :
            pos = (point[0,0], point[0,1])
            cv2.circle(frame, pos, 2, color=(0,255,255), thickness=-1)
            
    return frame


#영상 가져오기
vc = cv2.VideoCapture('./images/video4.MP4')
#스티커 가져오기
#img_sticker = cv2.imread('images/pngegg (6)')


while True :
    #영상을 frame으로 쪼개기
    _, frame = vc.read()
    #gray 스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #만들어놓은 얼굴 눈 찾기
    canvas = detect(gray, frame)
    #찾은 영상 보여주기
    cv2.imshow("canvas", canvas)
    
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

vc.release()
cv2.destroyAllWindows()
