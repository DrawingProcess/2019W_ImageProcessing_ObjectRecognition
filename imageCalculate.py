import cv2

image = cv2.imread('image_basic.png')
# 픽셀 수 및 이미지 크기 확인
print(image.shape)
print(image.size)

# 이미지 Numpy 객체의 특정 픽셀을 가리킵니다.
px = image[100, 100]

# B, G, R 순서로 출력됩니다.
# Gray Scale: B, G, R로 구분되지 않습니다.
print(px)

# R 값만 출력하기
print(px[2]) #B, G, R 순이므로