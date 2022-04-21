import cv2
import numpy as np
import time
import math


class LivePlot:
    def __init__(self, w=640, h=480, yLimit=[0, 100], multi_line = 2,
                 interval=0.001, invert=False, char=' '):

        self.yLimit = yLimit
        self.w = w
        self.h = h
        self.invert = invert
        self.interval = interval
        self.char = char[0]
        self.imgPlot = np.zeros((self.h, self.w, 3), np.uint8)
        self.imgPlot[:] = 225, 225, 225

        cv2.rectangle(self.imgPlot, (0, 0),
                      (self.w, self.h),
                      (0, 0, 0), cv2.FILLED)
        self.xP = 0
        self.yP = 0
        self.y_list_dictionary = {}
        for index in range(multi_line):
            self.y_list_dictionary[index] = []
            # self.y_list_dictionary[id] = []

        self.xList = [x for x in range(0, 100)]
        self.ptime = 0

    def update(self, y, id, color=(255, 0, 255)):
        if id == 1:
            color=(0, 0, 255)
        if time.time() - self.ptime > self.interval:

            # Refresh
            self.imgPlot[:] = 225, 225, 225
            # Draw Static Parts
            self.drawBackground()
            # Draw the text value
            cv2.putText(self.imgPlot, str(y),
                        (self.w - (125), 50), cv2.FONT_HERSHEY_PLAIN,
                        3, (150, 150, 150), 3)
            if self.invert:
                self.yP = int(np.interp(y, self.yLimit,
                                        [self.h, 0]))
            else:
                self.yP = int(np.interp(y, self.yLimit,
                                        [0, self.h]))
            self.y_list_dictionary[id].append(self.yP)
            # self.y_list_dictionary[id].append(self.yP)
            if len(self.y_list_dictionary[id]) == 100:
                self.y_list_dictionary[id].pop(0)
            for key, value in self.y_list_dictionary.items():
                for i in range(0, len(value)):
                    if i < 2:
                        pass
                    else:
                        cv2.line(self.imgPlot, (int((self.xList[i - 1] * (self.w // 100))) - (self.w // 10),
                                                value[i - 1]),
                                (int((self.xList[i] * (self.w // 100)) - (self.w // 10)),
                                value[i]), color, 2)
            self.ptime = time.time()

        return self.imgPlot

    def drawBackground(self):
        # Draw Background Canvas
        cv2.rectangle(self.imgPlot, (0, 0),
                      (self.w, self.h),
                      (0, 0, 0), cv2.FILLED)

        # Center Line
        cv2.line(self.imgPlot, (0, self.h // 2), (self.w, self.h // 2), (150, 150, 150), 2)

        # Draw Grid Lines
        for x in range(0, self.w, 50):
            cv2.line(self.imgPlot, (x, 0), (x, self.h),
                     (50, 50, 50), 1)

        for y in range(0, self.h, 50):
            cv2.line(self.imgPlot, (0, y), (self.w, y),
                     (50, 50, 50), 1)
            #  Y Label
            cv2.putText(self.imgPlot,
                        f'{int(self.yLimit[1] - ((y / 50) * ((self.yLimit[1] - self.yLimit[0]) / (self.h / 50))))}',
                        (10, y), cv2.FONT_HERSHEY_PLAIN,
                        1, (150, 150, 150), 1)
        cv2.putText(self.imgPlot, self.char,
                    (self.w - 100, self.h - 25), cv2.FONT_HERSHEY_PLAIN,
                    5, (150, 150, 150), 5)


def main():
    xPlot = LivePlot(w=1200, yLimit=[-100, 100], interval=0.01)
    x = 0
    while True:

        x += 1
        if x == 360: x = 0
        imgPlot = xPlot.update(int(math.sin(math.radians(x)) * 100),0)

        cv2.imshow("Image", imgPlot)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# if __name__ == "__main__":
#     main()
