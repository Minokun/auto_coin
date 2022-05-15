# -*- coding:utf-8 -*-

from paddleocr import PaddleOCR, draw_ocr
import cv2
import numpy as np

class DetectPic:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
        self.result = ''
        self.top_y_position = 380
        self.bottom_y_position = 2220
        self.top_list = []
        self.bottom_list = []

    def detect(self, img):
        self.result = self.ocr.ocr(img)

    def detect_top(self, img):
        self.detect(img)
        self.top_list = []
        for i in self.result:
            if i[0][3][1] < self.top_y_position:
                self.top_list.append(i)

    def detect_bottom(self, img):
        self.detect(img)
        self.bottom_list = []
        for i in self.result:
            if i[0][3][1] > self.bottom_y_position:
                self.bottom_list.append(i)


if __name__ == "__main__":
    detect_pic = DetectPic()
    detect_pic.detect_bottom('media/screen_QKXUT20329000108.png')
    for i in detect_pic.bottom_list:
        if i[1][0].find("首页") >= 0:
            print(i)