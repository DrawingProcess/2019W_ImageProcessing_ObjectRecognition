import cv2 as cv

def setLabel(image, str, contour):
    (text_width, text_height), baseline = cv.getTextSize(str, cv.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    x,y,width,height = cv.boundingRect(contour)
    pt_x = x+int((width-text_width)/2)
    pt_y = y+int((height + text_height)/2)
    cv.rectangle(image, (pt_x, pt_y+baseline), (pt_x+text_width, pt_y-text_height), (200,200,200), cv.FILLED)
    cv.putText(image, str, (pt_x, pt_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8)


img_color = cv.imread('../img/tray_ori.jpg', cv.IMREAD_COLOR)
cv.imshow('result', img_color)
cv.waitKey(0)

img_blur = cv.GaussianBlur(img_color, (3, 3), 0)
cv.imshow('result', img_blur)
cv.imwrite('../img/tray_blur.jpg', img_blur)

img_canny = cv.Canny(img_blur, 100, 300)
cv.imshow('result', img_canny)
cv.imwrite('../img/tray_canny.jpg', img_canny)

img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
cv.imshow('result', img_gray)
cv.imwrite('../img/tray_gray.jpg', img_gray)
cv.waitKey(0)

ret,img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
cv.imshow('result', img_binary)
cv.imwrite('../img/tray_binary.jpg', img_binary)
cv.waitKey(0)

contours, hierarchy = cv.findContours(img_binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    size = len(cnt)
    print(size)

    epsilon = 0.005 * cv.arcLength(cnt, True)
    approx = cv.approxPolyDP(cnt, epsilon, True)

    size = len(approx)
    print(size)

    cv.line(img_color, tuple(approx[0][0]), tuple(approx[size-1][0]), (0, 255, 0), 3)
    for k in range(size-1):
        cv.line(img_color, tuple(approx[k][0]), tuple(approx[k+1][0]), (0, 255, 0), 3)



cv.imshow('result', img_color)
cv.imwrite('../img/tray_contour.jpg', img_color)
cv.waitKey(0)