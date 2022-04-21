from matplotlib.pyplot import draw
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import cv2

cap = cv2.VideoCapture(r'Examples\video_test.mp4')
detector = FaceMeshDetector(maxFaces=1)
id_list = [22,23,24,26,110,157,158,159,160,161,130,243]
plotY = LivePlot(640,360,[20,50], 2)
while True:
    success, img = cap.read()
    if not success:
        break
    img, faces = detector.findFaceMesh(img, draw= False)
    if faces:
        face = faces[0]
        for id in id_list:
            cv2.circle(img, face[id],1,(255,0,255),cv2.FILLED)
        left_left = face[130]
        left_right = face[243]
        left_up = face[159]
        left_down = face[23]
        length_ver, _ = detector.findDistance(left_up, left_down)
        length_hor, _ = detector.findDistance(left_left, left_right)
        cv2.line(img, left_up, left_down, (0,200,0),3)
        cv2.line(img, left_left, left_right,(0,200,0),3)
        ratio = (length_ver/length_hor)*100
        img_plot = plotY.update(ratio,0)
        cv2.imshow("img_plot", img_plot)
        img_plot = plotY.update(ratio-50,1)
        cv2.imshow("img_plot1", img_plot)
    cv2.imshow("Image", img)
    cv2.waitKey(1)