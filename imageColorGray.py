import cv2

# OpenCV : [B, G, R] / Matplotlib : [R, G, B]
img_basic = cv2.imread('tray.jpg', cv2.IMREAD_COLOR)
cv2.imshow('Image Basic', img_basic)
cv2.waitKey(0)
cv2.imwrite('tray1.jpg', img_basic)

cv2.destroyAllWindows()

img_gray = cv2.cvtColor(img_basic, cv2.COLOR_BGR2GRAY)
cv2.imshow('Image Gray', img_gray)
cv2.waitKey(0)
cv2.imwrite('tray2.jpg', img_gray)
