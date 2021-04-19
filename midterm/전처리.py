import cv2

img = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
copy_img = img.copy()
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(img2, (3, 3), 0)

canny = cv2.Canny(blur, 100, 300)

cv2.imwrite('4.jpg', canny)







