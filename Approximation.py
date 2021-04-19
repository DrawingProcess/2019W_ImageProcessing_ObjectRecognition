import cv2 as cv

img_color = cv.imread('card4.jpg',cv.IMREAD_COLOR)
cv.imshow('result',img_color)
cv.waitKey(0)

img_gray = cv.cvtColor(img_color,cv.COLOR_BGR2GRAY)
cv.imshow('result',img_gray)
cv.waitKey(0)

ret,img_binary=cv.threshold(img_gray,127,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
cv.imshow('result',img_binary)

contours, hierarchy=cv.findContours(img_binary,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    size = len(cnt)
    print(size)

    epsilon = 0.4*cv.arcLength(cnt,True)
    approx=cv.approxPolyDP(cnt,epsilon,True)

    size=len(approx)
    print(size)

    cv.line(img_color,tuple(approx[0][0]),tuple(approx[size-1][0]),(0,255,0),3)
    for k in range(size-1):
        cv.line(img_color,tuple(approx[k][0]),tuple(approx[k+1][0]),(0,255,0),3)
        cv.imshow('result',img_color)

cv.waitKey(0)