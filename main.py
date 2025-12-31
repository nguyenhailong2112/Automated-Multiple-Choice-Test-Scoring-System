import cv2
import numpy as np
import support

from support import rectContour
from testform import questions, choices, answers

###################################################################

path = "C:/Users/longn/PycharmProjects/BTL_CHAMTHITN/.venv/DEMO0.png"

widthImg = 480
heightImg = 750

webcam = True
cameraNo = 0

################################################################

cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)

while True:
    # if webcam:
    #     success, img = cap.read()
    # else:
    img = cv2.imread(path)

    ## Tien xu ly anh

    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgFinal = img.copy()
    imgBiggestContours = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 50)

    try:
        ## Contours
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        ## Rectangles
        rectCon = support.rectContour(contours)
        biggestContours = support.getCornerPoints(rectCon[0])
        # print(biggestContours.shape)
        gradePoints = support.getCornerPoints(rectCon[1])
        # print(gradePoints)
        # print(biggestContours)

        if biggestContours.size !=0 and gradePoints.size !=0:
            cv2.drawContours(imgBiggestContours, biggestContours, -1, (0, 255, 0), 15)
            cv2.drawContours(imgBiggestContours, gradePoints, -1, (255, 0, 0), 15)

            biggestContours=support.reorder(biggestContours)
            gradePoints=support.reorder(gradePoints)

            pt1 = np.float32(biggestContours)
            pt2 = np.float32([[0,0],[widthImg,0],[0,heightImg],[widthImg,heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1,pt2)
            imgWarpColored = cv2.warpPerspective(imgContours, matrix, (widthImg, heightImg))
            # cv2.imshow("BAI THI TRAC NGHIEM", imgWarpColored)

            ptPoint1 = np.float32(gradePoints)
            ptPoint2 = np.float32([[0, 0], [120, 0], [0, 90], [120, 90]]) #[[  90][ 644][ 389][-165]]
            matrixPoint = cv2.getPerspectiveTransform(ptPoint1, ptPoint2)
            imgWarpColoredPoint = cv2.warpPerspective(imgContours, matrixPoint, (120, 90))
            # cv2.imshow("DIEM", imgWarpColoredPoint)

            # PHAT HIEN O TRAC NGHIEM
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 150, 255, cv2.THRESH_BINARY_INV)[1]
            # cv2.imshow("ĐỔI TRẮNG THAY ĐEN",imgThresh)

            boxes = support.splitBoxes(imgThresh)
            # cv2.imshow("TEST",boxes[0])
            # print(cv2.countNonZero(boxes[0]),cv2.countNonZero(boxes[1]),cv2.countNonZero(boxes[2]),cv2.countNonZero(boxes[3])) #5417 1284 1287 1826

            # KIỂM THU NHẬN PIXEL
            myPixelVal = np.zeros((questions,choices))
            countC = 0
            countR = 0
            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if (countC == choices):
                    countR += 1
                    countC = 0
            # print(myPixelVal)


            # lƯU CHỈ SỐ VỊ TRÍ CÁC Ô ĐƯỢC TÔ
            myIndex = []
            for x in range (0,questions):
                array = myPixelVal[x]
                # print("array",array)
                myIndexVal = np.where(array == np.amax(array))
                # print(myIndexVal[0])
                myIndex.append(int(myIndexVal[0][0]))
            print(myIndex)

            # GRADING
            grading = []
            for x in range (0,questions):
                if answers[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            # print(grading)

            # GRADE
            score = sum(grading)/questions *10
            print(score)

            # DISPLAYING ANS
            imgResult = imgWarpColored.copy()
            imgResult = support.showAnswers(imgResult, myIndex, grading, answers, questions, choices)
            imgRawDrawing = np.zeros_like(imgWarpColored)
            imgRawDrawing = support.showAnswers(imgRawDrawing, myIndex, grading, answers, questions, choices)

            invMatrix = cv2.getPerspectiveTransform(pt2, pt1)
            imgInvWarp = cv2.warpPerspective(imgRawDrawing, invMatrix, (widthImg, heightImg))

            # imgRawGrade = np.zeros_like(imgWarpColoredPoint)
            # cv2.putText(imgRawGrade, str(int(score)), (250, 100), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 255), 2)
            # cv2.imshow("Grade", imgRawGrade)

            # invMatrixPoint = cv2.getPerspectiveTransform(ptPoint2, ptPoint1)
            # imgInvWarpColoredPoint = cv2.warpPerspective(imgRawGrade, invMatrixPoint, (widthImg, heightImg))
            # imgInvWarpColoredPoint = cv2.cvtColor(imgInvWarpColoredPoint, cv2.COLOR_GRAY2BGR)
            # cv2.putText(imgInvWarpColoredPoint, str(int(score)), (250, 110), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 255, 255), 2)
            # cv2.imshow("Warped Grade", imgInvWarpColoredPoint)

            x, y, w, h = cv2.boundingRect(gradePoints)  # Lấy tọa độ contour "Điểm"
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.putText(imgFinal, str(score), (center_x - 35, center_y + 10),
                        cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)

            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            # imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarpColoredPoint, 1, 0)


        imgBlank = np.zeros_like(img)
        imageArray = ([img, imgGray, imgBlur, imgCanny, imgContours, imgBiggestContours],
                      [imgWarpColored, imgThresh, imgResult,imgRawDrawing,imgInvWarp,imgFinal])

    except:
        imgBlank = np.zeros_like(img)
        imageArray = [[img, imgBlank, imgBlank, imgBlank, imgBlank, imgBlank],
                      [imgBlank, imgBlank, imgBlank, imgBlank, imgBlank, imgBlank]]


    imgStacked = support.stackImage(imageArray, 0.5)


    cv2.imshow("FINAL RESULT", imgFinal)
    cv2.imshow("KET QUA CHAM THI", imgStacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("FinalResult.png", imgFinal)
        cv2.waitKey(300)

###############################################################################