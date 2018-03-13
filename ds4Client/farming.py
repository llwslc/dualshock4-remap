#!/usr/bin/python3

import tkinter as tk
import RPi.GPIO as GPIO
import threading
import time

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

farmFlag = False
attackTimer = 0
checkTimer = 0
cap = WebcamImageGetter()
cap.start()

# allow the camera to warmup
time.sleep(2)

# y x min
unknownItem = [276, 713, 200, 300]
knownItem = [276, 713, 0, 30]


def checkItem(col, target):
    checkFlag = True

    for i in range(len(col)):
        if col[i] > target[2] and col[i] < target[3]:
            pass
        else:
            checkFlag = False
            break

    return checkFlag

refreshTime = time.time()
def attackFunc():
    global attackTimer
    global refreshTime

    attackTime = 1
    sleepTime = 0.5
    attackTimer = threading.Timer(attackTime, attackFunc)
    attackTimer.start()

    # print(1/(time.time()-refreshTime), (time.time()-refreshTime))
    # refreshTime = time.time()

    GPIO.output(DS4_R1, GPIO.HIGH)
    GPIO.output(DS4_L2, GPIO.HIGH)
    GPIO.output(DS4_CIRCLE, GPIO.HIGH)

    time.sleep(sleepTime)

    GPIO.output(DS4_L2, GPIO.LOW)
    GPIO.output(DS4_R1, GPIO.LOW)
    GPIO.output(DS4_CIRCLE, GPIO.LOW)

def checkFunc():
    global checkTimer
    global refreshTime

    checkTime = 5
    pressTime = 0.01
    checkTimer = threading.Timer(checkTime, checkFunc)
    checkTimer.start()

    image = cap.getFrame()

    # print('item: ', image[unknownItem[0]][unknownItem[1]])

    if not checkItem(image[unknownItem[0]][unknownItem[1]], unknownItem):
        if checkItem(image[knownItem[0]][knownItem[1]], knownItem):
            # print('=======================> pick up')
            GPIO.output(DS4_CROSS, GPIO.LOW)
            time.sleep(pressTime)
            GPIO.output(DS4_CROSS, GPIO.HIGH)
        else:
            # print('=======================> ignore <===')
            GPIO.output(DS4_CROSS, GPIO.HIGH)
    else:
        # print('=======================> ignore')
        GPIO.output(DS4_CROSS, GPIO.HIGH)

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
def pressFarm():
    global farmFlag
    global attackTimer
    global checkTimer
    if farmFlag:
        btnFarm['bg'] = 'red'
        farmFlag = False
        attackTimer.cancel()
        checkTimer.cancel()
        time.sleep(2)
        GPIO.output(DS4_R1, GPIO.HIGH)
        GPIO.output(DS4_L2, GPIO.HIGH)
        GPIO.output(DS4_CROSS, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    else:
        btnFarm['bg'] = 'green'
        farmFlag = True
        attackTimer = threading.Timer(1, attackFunc)
        attackTimer.start()
        checkTimer = threading.Timer(1, checkFunc)
        checkTimer.start()

def handleClose():
    global attackTimer
    global checkTimer
    if attackTimer != 0:
        attackTimer.cancel()
    if checkTimer != 0:
        checkTimer.cancel()
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
btnFarm = tk.Button(root, text = 'Farm', bg = 'red', height = btnHeight, width = btnWidth)
btnFarm['command'] = pressFarm
btnFarm.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnQuit = tk.Button(root, text = 'QUIT', height = btnHeight, width = btnWidth, fg = 'red', command = handleClose)
btnQuit.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)


root.protocol("WM_DELETE_WINDOW", handleClose)

try:
    root.mainloop()
except KeyboardInterrupt:
    handleClose()