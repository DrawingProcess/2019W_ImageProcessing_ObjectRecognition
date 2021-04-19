import cv2
import numpy as np
from scipy.spatial import distance as dist


def setLabel(image, str, contour):

   fontface = cv2.FONT_HERSHEY_SIMPLEX
   scale = 0.6
   thickness = 2

   size = cv2.getTextSize(str, fontface, scale, thickness)
   text_width = size[0][0]
   text_height = size[0][1]

   x, y, width, height = cv2.boundingRect(contour)

   pt = (x + int((width - text_width) / 2), y + int((height + text_height) / 2))
   cv2.putText(image, str, pt, fontface, scale, (255, 255, 255), thickness, 8)



# 컨투어 내부의 색을 평균내서 red, green, blue 중 어느 색인지 체크
def label(image, contour):


   mask = np.zeros(image.shape[:2], dtype="uint8")
   cv2.drawContours(mask, [contour], -1, 255, -1)

   mask = cv2.erode(mask, None, iterations=2)
   mean = cv2.mean(image, mask=mask)[:3]


   minDist = (np.inf, None)



   for (i, row) in enumerate(lab):

       d = dist.euclidean(row[0], mean)

       if d < minDist[0]:
           minDist = (d, i)

   return colorNames[minDist[1]]



# 인식할 색 입력
colors = [[0, 0, 255], [0, 255, 0], [255, 0, 0]]
colorNames = ["red", "green", "blue"]



lab = np.zeros((len(colors), 1, 3), dtype="uint8")
for i in range(len(colors)):
   lab[i] = colors[i]

lab = cv2.cvtColor(lab, cv2.COLOR_BGR2LAB)




# 원본 이미지 불러오기
image = cv2.imread("card3.jpg", 1)


blurred = cv2.GaussianBlur(image, (5, 5), 0)

# 이진화
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 152, 255, cv2.THRESH_BINARY)

# 색검출할 색공간으로 LAB사용
img_lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

thresh = cv2.erode(thresh, None, iterations=2)
cv2.imshow("Thresh", thresh)


# 컨투어 검출
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# 컨투어 리스트가 OpenCV 버전에 따라 차이있기 때문에 추가
if len(contours) == 2:
   contours = contours[0]

elif len(contours) == 3:
   contours = contours[1]


# 컨투어 별로 체크
for contour in contours:

   cv2.imshow("Image", image)
   cv2.waitKey(0)

   # 컨투어를 그림
   cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)


   # 컨투어 내부에 검출된 색을 표시
   color_text = label(img_lab, contour)
   setLabel(image, color_text, contour)


cv2.imshow("Image", image)
cv2.waitKey(0)