from matplotlib.pyplot import axis, draw
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import cv2
import time
import numpy as np
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
id_list = [22,23,24,26,110,157,158,159,160,161,130,243]
plotY = LivePlot(640,360,[10,60], 3)
face_ratio = []
while True:
    success, img = cap.read()
    if not success:
        break
    img, faces = detector.findFaceMesh(img, draw= True)
    if faces:
        face = faces[0]
        # for id in id_list:
        #     cv2.circle(img, face[id],1,(255,0,255),cv2.FILLED)
        left_left = face[130]
        left_right = face[243]
        left_up = face[159]
        left_down = face[23]
        left_length_ver, _ = detector.findDistance(left_up, left_down)
        left_length_hor, _ = detector.findDistance(left_left, left_right)
        # cv2.line(img, left_up, left_down, (0,200,0),3)
        # cv2.line(img, left_left, left_right,(0,200,0),3)
        left_ratio = (left_length_ver/left_length_hor)*100

        right_left = face[463]
        right_right = face[263]
        right_up = face[386]
        right_down = face[253]
        right_length_ver, _ = detector.findDistance(right_up, right_down)
        right_length_hor, _ = detector.findDistance(right_left, right_right)
        right_ratio = (right_length_ver/right_length_hor)*100
        ave_ratio = (right_ratio + left_ratio)/2

        # forehead to nose
        forehead2nose_distance, _ = detector.findDistance(face[8], face[197])
        img_plot = plotY.update(forehead2nose_distance/2,1)
        time.sleep(0.01)

        eye2eye_distance, _ = detector.findDistance(left_down, right_down)
        print(right_length_hor/ eye2eye_distance)
        img_plot = plotY.update(eye2eye_distance/2,2)
        time.sleep(0.01)

        current_face_ratio = forehead2nose_distance/eye2eye_distance
        if len(face_ratio) < 20:
            face_ratio.append(current_face_ratio)
            face_ratio_mean = np.mean(face_ratio, axis = 0)
        multiple_ratio = face_ratio_mean/current_face_ratio

        img_plot = plotY.update(ave_ratio*multiple_ratio,0)

        cv2.imshow("img_plot1", img_plot)
    cv2.imshow("Image", img)
    cv2.waitKey(1)