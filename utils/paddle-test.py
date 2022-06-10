from paddleocr import PaddleOCR, draw_ocr
import math

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = '../media/227.png'
result = ocr.ocr(img_path, cls=True)

button_text = '我的现金'

for line in result:
    pass
#     # 如果找到了该位置
#     if line[1][0].find(button_text) >= 0 and line[0][0][1] >= (y_ad - 80) and line[0][0][1] <= (y_ad + 80):
#         x, y = int((line[0][0][0] + line[0][1][0]) / 2), int((line[0][0][1] + line[0][1][1]) / 2)
# print(x, y)

# 显示结果
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

