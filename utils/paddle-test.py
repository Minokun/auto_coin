from paddleocr import PaddleOCR, draw_ocr
import re
import math

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = '../media/124.png'
result = ocr.ocr(img_path, cls=True)
y_bottom_limit = 0
y_top_limit = 0

for line in result:
    if line[1][0].find('我的金币') >= 0:
        y_top_limit = line[0][2][1]
        break
crash_stats = False
coin_stats = False
for line in result:
    if line[0][0][1] > y_top_limit:
        if line[1][0].find('.') >= 0:
            print(line[1][0])
            g = re.findall(r'^.*?万.*?([\d]+\.[\d]+)元$', line[1][0])
            if len(g) > 0:
                cash = g[0]
                cash_stats = True

        g = re.findall(r'^([\d]+)$', line[1][0])
        if len(g) > 0:
            coin = g[0]
            coin_stats = True
    if crash_stats and coin_stats:
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