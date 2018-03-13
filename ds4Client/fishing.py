#!/usr/bin/python3

import tkinter as tk
import RPi.GPIO as GPIO
import threading
import kmeans
import time

from PIL import Image
from capture import WebcamImageGetter

# initialize GPIO
DS4_L1 = 16
DS4_L2 = 36
DS4_R1 = 18
DS4_R2 = 38
DS4_UP = 40
DS4_SQUARE = 33
DS4_TRIANGLE = 35
DS4_CIRCLE = 37
DS4_CROSS = 31
DS4_PS = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DS4_L1, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_L2, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_R1, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_R2, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_UP, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_SQUARE, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_TRIANGLE, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_CIRCLE, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_CROSS, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_PS, GPIO.OUT, initial = GPIO.HIGH)

btnHeight = 3
btnWidth = 10
btnPad = 10
btnRowIndex = 0
btnColIndex = 0

fishFlag = False
fishTimer = 0
cap = WebcamImageGetter()
cap.start()

# allow the camera to warmup
time.sleep(2)

# y x min max
activeR2 = [620, 820, 60, 80]
activeL2 = [630, 460, 60, 80]
activeUP = [630, 540, 60, 80]

# y start - y end corner and x start - x end corner
activeSQUARE = [640, 670, 680, 710]
activeTRIANGLE = [620, 650, 720, 750]
activeCIRCLE = [640, 670, 760, 790]


def checkActive(col, target):
    activeFlag = False

    for i in range(len(col)):
        if col[i] < target[2] or col[i] > target[3]:
            activeFlag = True
            break

    return activeFlag

def getMainColor(imageData):
    blueFlag = False
    image = Image.fromarray(imageData, 'RGB')
    pixels = [] # [(r,g,b), count]
    for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
        pixels.append([(r, g, b), count])
    try:
        colors = kmeans.kmeans(pixels, 3)
    except:
        return blueFlag

    # image data is BGR
    for (r, g, b) in colors:
        if r > 100:
            blueFlag = True
    return blueFlag


refreshTime = time.time()
def fishFunc():
    global fishTimer
    global refreshTime

    frameTime = 0.5
    sleepTime = 0.3
    fishTimer = threading.Timer(frameTime, fishFunc)
    fishTimer.start()

    # print(1/(time.time()-refreshTime), (time.time()-refreshTime))
    # refreshTime = time.time()

    image = cap.getFrame()

    if checkActive(image[activeR2[0]][activeR2[1]], activeR2):
        GPIO.output(DS4_R2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(DS4_R2, GPIO.HIGH)

    if checkActive(image[activeL2[0]][activeL2[1]], activeL2):
        GPIO.output(DS4_L2, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(DS4_L2, GPIO.HIGH)

    if checkActive(image[activeUP[0]][activeUP[1]], activeUP):
        GPIO.output(DS4_UP, GPIO.LOW)
        time.sleep(sleepTime)
        GPIO.output(DS4_UP, GPIO.HIGH)

    if getMainColor(image[activeSQUARE[0]:activeSQUARE[1], activeSQUARE[2]:activeSQUARE[3]]):
        # print('=======================> square')
        GPIO.output(DS4_SQUARE, GPIO.LOW)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    elif getMainColor(image[activeTRIANGLE[0]:activeTRIANGLE[1], activeTRIANGLE[2]:activeTRIANGLE[3]]):
        # print('=======================> triangle')
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.LOW)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    elif getMainColor(image[activeCIRCLE[0]:activeCIRCLE[1], activeCIRCLE[2]:activeCIRCLE[3]]):
        # print('=======================> circle')
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.LOW)
    else:
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)

def pressPS():
    GPIO.output(DS4_PS, GPIO.LOW)
    time.sleep(1)
    GPIO.output(DS4_PS, GPIO.HIGH)
    time.sleep(1)
def pressX():
    GPIO.output(DS4_CROSS, GPIO.LOW)
    time.sleep(1)
    GPIO.output(DS4_CROSS, GPIO.HIGH)
    time.sleep(1)
def pressO():
    GPIO.output(DS4_CIRCLE, GPIO.LOW)
    time.sleep(1)
    GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    time.sleep(1)
def pressR1():
    GPIO.output(DS4_R1, GPIO.LOW)
    time.sleep(1)
    GPIO.output(DS4_R1, GPIO.HIGH)
    time.sleep(1)
def pressFish():
    global fishFlag
    global fishTimer
    if fishFlag:
        btnFish['bg'] = 'red'
        fishFlag = False
        fishTimer.cancel()
        time.sleep(2)
        GPIO.output(DS4_R2, GPIO.HIGH)
        GPIO.output(DS4_L2, GPIO.HIGH)
        GPIO.output(DS4_UP, GPIO.HIGH)
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    else:
        btnFish['bg'] = 'green'
        fishFlag = True
        fishTimer = threading.Timer(1, fishFunc)
        fishTimer.start()

def handleClose():
    if fishTimer != 0:
        fishTimer.cancel()
    cap.stop()
    root.destroy()
    GPIO.cleanup()

root = tk.Tk()
root.geometry('+0+0')

btnPS = tk.Button(root, text = 'PS', height = btnHeight, width = btnWidth)
btnPS['command'] = pressPS
btnPS.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnX = tk.Button(root, text = 'X', height = btnHeight, width = btnWidth)
btnX['command'] = pressX
btnX.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnO = tk.Button(root, text = 'O', height = btnHeight, width = btnWidth)
btnO['command'] = pressO
btnO.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)


btnRowIndex = btnRowIndex + 1
btnColIndex = 0
btnFish = tk.Button(root, text = 'Fish', bg = 'red', height = btnHeight, width = btnWidth)
btnFish['command'] = pressFish
btnFish.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnR1 = tk.Button(root, text = 'R1', height = btnHeight, width = btnWidth)
btnR1['command'] = pressR1
btnR1.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnQuit = tk.Button(root, text = 'QUIT', height = btnHeight, width = btnWidth, fg = 'red', command = handleClose)
btnQuit.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)


root.protocol("WM_DELETE_WINDOW", handleClose)

try:
    root.mainloop()
except KeyboardInterrupt:
    handleClose()