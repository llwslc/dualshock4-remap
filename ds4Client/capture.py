#!/usr/bin/python3

import threading
import cv2

class WebcamImageGetter:

    def __init__(self):
        self.stopFlag = True
        self.currentFrame = [[0,0,0]]

        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, 1920)
        self.capture.set(4, 1080)

    def start(self):
        threading.Thread(target=self.updateFrame, args=()).start()

    def updateFrame(self):
        while(self.stopFlag):
            ret, self.currentFrame = self.capture.read()

            # cv2.imshow('img', self.currentFrame[640:670, 760:790])
            # cv2.waitKey(0)

    def stop(self):
        self.stopFlag = False
        self.capture.release()
        cv2.destroyAllWindows()

    def getFrame(self):
        return self.currentFrame
