from paddleocr import PaddleOCR, draw_ocr
import re
import math

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = '../media/1.png'
result = ocr.ocr(img_path, cls=True)

button_text = '我的现金'
coin = 1111
cash = 1111
for line in result:
    if line[0][0][1] > 230:
        if line[1][0].find('.') >= 0:
            g = re.findall(r'[^\d]*([\d]+\.[\d]+)元*', line[1][0])
            if len(g) > 0:
                cash = float(g[0])
        g = re.findall(r'^([\d]+)[币]*$', line[1][0])
        if len(g) > 0:
            coin = float(g[0])
            break
print(cash, coin)
# 显示结果
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

