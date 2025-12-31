import cv2
import numpy as np

from numpy.ma.testutils import approx

from testform import questions, choices, answers

def stackImage(imgArray, scale, labels=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])

    # Resize all images in the array at once
    resized_images = [
        [cv2.resize(img, (0, 0), None, scale, scale) if len(img.shape) == 3 else cv2.cvtColor(cv2.resize(img, (0, 0), None, scale, scale), cv2.COLOR_GRAY2BGR)
         for img in row] for row in imgArray
    ]

    # Concatenate images horizontally and vertically
    hor_stack = [np.hstack(row) for row in resized_images]
    ver_stack = np.vstack(hor_stack)

    # Add labels if necessary
    if labels:
        eachImgWidth = ver_stack.shape[1] // cols
        eachImgHeight = ver_stack.shape[0] // rows
        for d in range(cols):
            for c in range(rows):
                cv2.rectangle(ver_stack,
                              (c * eachImgWidth, d * eachImgHeight),
                              (c * eachImgWidth + len(labels[d][c]) * 13 + 27, 30 + eachImgHeight),
                              (0, 255, 0), 2)  # Adjust the rectangle thickness here
                cv2.putText(ver_stack,
                            labels[d][c],
                            (eachImgWidth * c + 10, eachImgHeight * d + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    return ver_stack


def rectContour(contours):
    rectCon = []
    for i in contours:
        area = cv2.contourArea(i)
        # print("Area",area)
        if area > 1000:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            # print("Corner Points", len(approx))
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    return rectCon

def getCornerPoints(contours):
    peri = cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, 0.02*peri, True)
    return approx

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2), np.int32)

    add = myPoints.sum(axis=1)
    # print(myPoints)
    # print(add)
    myPointsNew[0] = myPoints[np.argmin(add)] # [0,0]
    myPointsNew[3] = myPoints[np.argmax(add)] # [width,height]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)] # [width,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] # [0,height]
    # print(diff)

    return myPointsNew

def splitBoxes(img):
    rows = np.vsplit(img, 10)
    boxes = []

    for r in rows:
        cols = np.hsplit(r, 4)
        for box in cols:
            boxes.append(box)
            # cv2.imshow("Split", box)
    return boxes

def showAnswers(img, myIndex, grading, answers, questions, choices):
    secW = int(img.shape[1]/choices)  # Chiều rộng của mỗi ô
    secH = int(img.shape[0]/questions)  # Chiều cao của mỗi ô

    for x in range(0, questions):
        myAns = myIndex[x]  # Đáp án người dùng tô
        cX = (myAns * secW) + secW // 2
        cY = (x * secH) + secH // 2

        if grading[x] == 1:
            cv2.circle(img, (int(cX), int(cY)), 30, (0, 255, 0), cv2.FILLED)
        else:
            cv2.circle(img, (int(cX), int(cY)), 30, (0, 0, 255), cv2.FILLED)

        # Hiển thị đáp án đúng ở màu xanh viền
        correctX = (answers[x] * secW) + secW // 2
        correctY = cY
        cv2.circle(img, (int(correctX), int(correctY)), 20, (0, 255, 0), 5)  # Viền xanh cho đáp án đúng

    return img
