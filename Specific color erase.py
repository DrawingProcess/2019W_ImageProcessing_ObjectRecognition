import cv2
image = cv2.imread('card.jpg')
# 특정 색상만 보여주기 (0: Blue, 1: Green, 2: Red)
cv2.imshow('Image', image[:, :, 0])
cv2.waitKey(0)

# 특정 색상만 제거하기
image[:, :, 2] = 0
cv2.imshow('Image', image)
cv2.waitKey(0)