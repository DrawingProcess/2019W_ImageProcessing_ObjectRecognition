# opencv - 명함인식 구현하기 (웹캠)
import numpy as np
import cv2


def order_points(pts):
    rect = np.zeros((4, 2), dtype='float32')

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def auto_scan_image_via_webcam():
    try:
        cap = cv2.VideoCapture(0) # VideoCapture() 함수는 카메라를 불러오는 함수이다.
    except:
        print('Cannot load Camera!')

    # 계속해서 루프를 돈다. ESC키를 누르기 전까지.
    while True:
      ret, frame = cap.read() # 루프를 돌면서 계속해서 카메라로부터 프레임을 받아온다.
      if ret == True:
        k = cv2.waitKey(10) # 10ms를 기다림. () or (0)으로 할 시 무한정 기다림.
        if k == 27: # ESC : 27, space : 32
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0) # 이미지의 Gaussian Noise (백색노이즈, 전체적으로 밀도가 동일한 노이즈)를 제거하는 데 가장 효과적
        edged = cv2.Canny(gray, 75, 200) # 75보다 작을경우 거의 무시, 200보다 클경우 선명, 나머지 so-so

        print("STEP 1: Edge Detection")

        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        for c in cnts:
            # Contour 근사법(contour approximation) : 근사치의 최대거리를 0.02로 설정하여 실제 contour보다 각지게 표현
            # 도평의 외곽선을 꼭지점수가 원래보다 적은 다른 모양으로 바꾸고 싶을 때 사용! Douglas-Peucker 알고리즘을 적용하여 꼭지점 줄이기 근사를 수행!
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            # (x, y, w, h) = cv2.boundingRect(c)
            # if cv2.contourArea(c) < 900:
            #     continue
            # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

            screenCnt = []

            if len(approx) == 4:
                contourSize = cv2.contourArea(approx)
                # 불필요한 사각형을 검출하지 않기 위한 로직. 전체화면에 10% 이상을 차지할 때만 사각형을 검출하도록 함.
                camSize = frame.shape[0] * frame.shape[1]  # 받아들인 프레임에 가로 길이(frame.shape[0])와 세로 길이(frame.shape[1])를 곱한 것이 캠코더 사이즈.
                ratio = contourSize / camSize  # 영상사이즈 대비 외곽의 사이즈의 비율을 구해서
                print(contourSize)
                print(camSize)
                print(ratio)

                if ratio > 0.01 :  # 10%를 넘었을 때만 외곽을 검출하도록 함
                    screenCnt = approx
                break

                # 만약 추출한 외곽이 없다면 그냥 웹캠의 화면을 보여줌
        if len(screenCnt) == 0:
            cv2.imshow("WebCam", frame)
            continue
        else:  # 만약 추출한 외곽이 있다면 웹캠화면 위에 외곽을 drawContours()함수를 통해 그린 다음에 화면에 보여줌.
            print("STEP 2: Find contours of paper")

            cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2) # (대상이미지, contour, 음수시 모든 contour그림, GREEN, 선의 두께)
            cv2.imshow("WebCam", frame)

            # Rotated Rectangle
            # rect = cv2.minAreaRect(frame)
            # box = cv2.boxPoints(rect)
            # box = box.astype('int')
            # frame = cv2.drawContours(frame, [box], -1, 7)  # blue
            # cv2.imshow("WebCam", frame)

            rect = order_points(screenCnt.reshape(4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = rect

            w1 = abs(bottomRight[0] - bottomLeft[0])
            w2 = abs(topRight[0] - topLeft[0])
            h1 = abs(topRight[1] - bottomRight[1])
            h2 = abs(topLeft[1] - bottomLeft[1])
            maxWidth = max([w1, w2])
            maxHeight = max([h1, h2])

            dst = np.float32([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]])

            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))

            # print("STEP 3: Apply Perspective Transform")
            #
            # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            # warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
            #
            # print("STEP 4: Apply Adaptive Threshold")
      else:
        print('Cannot load Camera!')
        break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    cv2.imshow("Scanned", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    auto_scan_image_via_webcam()