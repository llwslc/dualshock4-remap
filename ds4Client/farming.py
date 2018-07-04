#!/usr/bin/python3

import tkinter as tk
import RPi.GPIO as GPIO
import threading
import dhash
import time
import cv2

from PIL import Image
from capture import WebcamImageGetter

# initialize GPIO MAP [PIN Default Active]
DS4_L1 = [16, GPIO.HIGH, GPIO.LOW]
DS4_L2 = [36, GPIO.LOW, GPIO.HIGH]
DS4_R1 = [18, GPIO.HIGH, GPIO.LOW]
DS4_R2 = [38, GPIO.LOW, GPIO.HIGH]
DS4_UP = [40, GPIO.HIGH, GPIO.LOW]
DS4_SQUARE = [33, GPIO.HIGH, GPIO.LOW]
DS4_TRIANGLE = [35, GPIO.HIGH, GPIO.LOW]
DS4_CIRCLE = [37, GPIO.HIGH, GPIO.LOW]
DS4_CROSS = [31, GPIO.HIGH, GPIO.LOW]
DS4_PS = [29, GPIO.HIGH, GPIO.LOW]
DS4_LX = [32, GPIO.LOW, GPIO.HIGH]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DS4_L1[0], GPIO.OUT, initial = DS4_L1[1])
GPIO.setup(DS4_L2[0], GPIO.OUT, initial = DS4_L2[1])
GPIO.setup(DS4_R1[0], GPIO.OUT, initial = DS4_R1[1])
GPIO.setup(DS4_R2[0], GPIO.OUT, initial = DS4_R2[1])
GPIO.setup(DS4_UP[0], GPIO.OUT, initial = DS4_UP[1])
GPIO.setup(DS4_SQUARE[0], GPIO.OUT, initial = DS4_SQUARE[1])
GPIO.setup(DS4_TRIANGLE[0], GPIO.OUT, initial = DS4_TRIANGLE[1])
GPIO.setup(DS4_CIRCLE[0], GPIO.OUT, initial = DS4_CIRCLE[1])
GPIO.setup(DS4_CROSS[0], GPIO.OUT, initial = DS4_CROSS[1])
GPIO.setup(DS4_PS[0], GPIO.OUT, initial = DS4_PS[1])
GPIO.setup(DS4_LX[0], GPIO.OUT, initial = DS4_LX[1])


btnHeight = 3
btnWidth = 10
btnPad = 10
btnRowIndex = 0
btnColIndex = 0

farmFlag = False
ignoreFlag = True
attackTimer = 0
checkTimer = 0
cap = WebcamImageGetter()
cap.start()

# allow the camera to warmup
time.sleep(2)

# y x min
unknownItem = [414, 1071, 200, 300]
knownItem = [414, 1071, -1, 35]
checkItem1 = [355, 1000, -1, 35]
checkItem2 = [355, 1185, -1, 35]
checkItem3 = [355, 1370, -1, 35]

enchLv5Item = [378, 408, 1238, 1318]

def getImgHash(img):
    row, col = dhash.dhash_row_col(img)
    mHash = dhash.format_hex(row, col)
    mHash = '0x' + mHash

    return int(mHash, 16)

enchLv5ImgHash = getImgHash(Image.open('enchLv5.bmp'))

def getEnchLevel(imageData):
    COMPARE_PERCENTAGE = 15
    lv5Flag = False

    b, g, r = cv2.split(imageData)
    rgbImg = cv2.merge([r, g, b])

    img = Image.fromarray(rgbImg, 'RGB')

    mBash = getImgHash(img)
    if dhash.get_num_bits_different(mBash, enchLv5ImgHash) < COMPARE_PERCENTAGE:
        lv5Flag = True
    else:
        pass

    return lv5Flag

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
    global farmFlag

    if not farmFlag:
        return

    attackTime = 1
    sleepTime = 0.5
    attackTimer = threading.Timer(attackTime, attackFunc)
    attackTimer.start()

    # print(1/(time.time()-refreshTime), (time.time()-refreshTime))
    # refreshTime = time.time()

    GPIO.output(DS4_R1[0], DS4_R1[2])
    GPIO.output(DS4_L2[0], DS4_L2[2])
    GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[2])

    time.sleep(sleepTime)

    GPIO.output(DS4_R1[0], DS4_R1[1])
    GPIO.output(DS4_L2[0], DS4_L2[1])
    GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])

def checkFunc():
    global checkTimer
    global refreshTime
    global farmFlag

    if not farmFlag:
        return

    checkTime = 3
    pressTime = 0.01
    checkTimer = threading.Timer(checkTime, checkFunc)
    checkTimer.start()

    image = cap.getFrame()

    if ignoreFlag:
        if getEnchLevel(image[enchLv5Item[0]:enchLv5Item[1], enchLv5Item[2]:enchLv5Item[3]]):
            GPIO.output(DS4_CROSS[0], DS4_CROSS[2])
            time.sleep(pressTime)
            GPIO.output(DS4_CROSS[0], DS4_CROSS[1])
    else:
        # print('unknownItem: ', image[unknownItem[0]][unknownItem[1]])
        # print('knownItem: ', image[knownItem[0]][knownItem[1]])
        # print('checkItem1: ', image[checkItem1[0]][checkItem1[1]])
        # print('checkItem2: ', image[checkItem2[0]][checkItem2[1]])
        # print('checkItem3: ', image[checkItem3[0]][checkItem3[1]])

        if not checkItem(image[unknownItem[0]][unknownItem[1]], unknownItem):
            if checkItem(image[knownItem[0]][knownItem[1]], knownItem):
                if checkItem(image[checkItem1[0]][knownItem[1]], checkItem1):
                    if checkItem(image[checkItem2[0]][checkItem2[1]], checkItem2):
                        if checkItem(image[checkItem3[0]][checkItem3[1]], checkItem3):
                            # print('=======================> pick up')
                            # print('unknownItem: ', image[unknownItem[0]][unknownItem[1]])
                            # print('knownItem: ', image[knownItem[0]][knownItem[1]])
                            # print('checkItem1: ', image[checkItem1[0]][checkItem1[1]])
                            # print('checkItem2: ', image[checkItem2[0]][checkItem2[1]])
                            # print('checkItem3: ', image[checkItem3[0]][checkItem3[1]])
                            GPIO.output(DS4_CROSS[0], DS4_CROSS[2])
                            time.sleep(pressTime)
                            GPIO.output(DS4_CROSS[0], DS4_CROSS[1])
            else:
                # print('=======================> ignore <===')
                GPIO.output(DS4_CROSS[0], DS4_CROSS[1])
        else:
            # print('=======================> ignore')
            GPIO.output(DS4_CROSS[0], DS4_CROSS[1])

def pressPS():
    GPIO.output(DS4_PS[0], DS4_PS[2])
    time.sleep(1)
    GPIO.output(DS4_PS[0], DS4_PS[1])
    time.sleep(1)
def pressX():
    GPIO.output(DS4_CROSS[0], DS4_CROSS[2])
    time.sleep(1)
    GPIO.output(DS4_CROSS[0], DS4_CROSS[1])
    time.sleep(1)
def pressO():
    GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[2])
    time.sleep(1)
    GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])
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
        GPIO.output(DS4_R1[0], DS4_R1[1])
        GPIO.output(DS4_L2[0], DS4_L2[1])
        GPIO.output(DS4_CROSS[0], DS4_CROSS[1])
        GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])
    else:
        btnFarm['bg'] = 'green'
        farmFlag = True
        attackTimer = threading.Timer(1, attackFunc)
        attackTimer.start()
        checkTimer = threading.Timer(1, checkFunc)
        checkTimer.start()
def pressIgnore():
    global ignoreFlag
    if ignoreFlag:
        btnIgnore['bg'] = 'red'
        btnIgnore['text'] = 'keep'
        ignoreFlag = False
    else:
        btnIgnore['bg'] = 'green'
        btnIgnore['text'] = 'ignore'
        ignoreFlag = True

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
btnIgnore = tk.Button(root, text = 'ignore', bg = 'green', height = btnHeight, width = btnWidth)
btnIgnore['command'] = pressIgnore
btnIgnore.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
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