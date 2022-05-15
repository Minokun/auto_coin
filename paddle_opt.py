# -*- coding:utf-8 -*-

from paddleocr import PaddleOCR, draw_ocr
import cv2
import numpy as np

class DetectPic:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
        self.result = ''

    def detect(self, img):
        self.result = self.ocr.ocr(img)

    def detect_top(self, img):
        if isinstance(img, np.ndarray) and len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)