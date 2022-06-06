# -*- coding:utf-8 -*-

from paddleocr import PaddleOCR, draw_ocr
import cv2
import numpy as np

class DetectPic:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
        self.top_y_position = 380
        self.bottom_y_position = 2220
        self.top_list = []
        self.bottom_list = []

    def detect(self, img):
        return self.ocr.ocr(img)

    def detect_top(self, img):
        result = self.detect(img)
        self.top_list = []
        if not result:
            return ''
        for i in result:
            if i[0][3][1] < self.top_y_position:
                self.top_list.append(i)
        return result

    def detect_bottom(self, img):
        result = self.detect(img)
        self.bottom_list = []
        if not result:
            return ''
        for i in result:
            if i[0][3][1] > self.bottom_y_position:
                self.bottom_list.append(i)
        return result


paddle_ocr_obj = DetectPic()

if __name__ == "__main__":
    detect_pic = DetectPic()
    result = detect_pic.detect_bottom('media/screen_192.168.101.101.png')
    print(result)

    for i in detect_pic.bottom_list:
        if i[1][0].find("领金币") >= 0:
            print(i)