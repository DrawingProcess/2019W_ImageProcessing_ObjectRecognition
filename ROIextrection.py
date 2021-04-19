import cv2
image = cv2.imread('card.jpg')

# Numpy Slicing: ROI 처리 가능
logo = image[20:150, 70:200]
cv2.imshow('Image', logo)
cv2.waitKey(0)

# ROI 단위로 이미지 복사하기
image[0:130, 0:130] = logo
cv2.imshow('Image', image)
cv2.waitKey(0)