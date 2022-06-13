from paddleocr import PaddleOCR, draw_ocr
import re
import math

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = '../media/212.png'
result = ocr.ocr(img_path, cls=True)
y_limit = 0
y_limit = 0
for line in result:
    if line[1][0].find('金币收益') >= 0:
        y_limit = line[0][2][1]
    if line[1][0].find('自动兑换现金') >= 0:
        y_limit_2 = line[0][0][1]
        break

for line in result:
    if line[0][0][1] > y_limit and line[0][0][1] < y_limit_2:
        if '.'.find(line[1][0]) >= 0:
            cash = float(line[1][0])
            print(cash)
        g = re.findall(r'^([\d]+)$', line[1][0])
        if len(g) > 0:
            print(g[0])

# 显示结果
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

