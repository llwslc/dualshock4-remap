#!/usr/bin/python3

import tkinter as tk
import RPi.GPIO as GPIO
import threading
import kmeans
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

fishFlag = False
ignoreFlag = False
fishTimer = 0
cap = WebcamImageGetter()
cap.start()

# allow the camera to warmup
time.sleep(2)

# y x min max
activeR2 = [930, 1230, 60, 80]
activeL2 = [945, 690, 60, 80]
activeUP = [945, 810, 60, 80]

# y start - y end corner and x start - x end corner
activeSQUARE = [963, 1006, 1023, 1066]
activeTRIANGLE = [933, 976, 1083, 1126]
activeCIRCLE = [963, 1006, 1143, 1186]

fishLevel = [949, 967, 949, 967]

def getImgHash(img):
    row, col = dhash.dhash_row_col(img)
    mHash = dhash.format_hex(row, col)
    mHash = '0x' + mHash

    return int(mHash, 16)

fishLv1ImgHash = getImgHash(Image.open('fishLv1.bmp'))
fishLv2ImgHash = getImgHash(Image.open('fishLv2.bmp'))
fishLv3ImgHash = getImgHash(Image.open('fishLv3.bmp'))

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
    for (b, g, r) in colors:
        if b > 100:
            blueFlag = True
    return blueFlag

def getFishLevel(imageData):
    COMPARE_PERCENTAGE = 15
    lowRankFlag = False

    b, g, r = cv2.split(imageData)
    rgbImg = cv2.merge([r, g, b])

    img = Image.fromarray(rgbImg, 'RGB')

    mBash = getImgHash(img)
    if dhash.get_num_bits_different(mBash, fishLv1ImgHash) < COMPARE_PERCENTAGE:
        lowRankFlag = True
    elif dhash.get_num_bits_different(mBash, fishLv2ImgHash) < COMPARE_PERCENTAGE:
        lowRankFlag = True
    elif dhash.get_num_bits_different(mBash, fishLv3ImgHash) < COMPARE_PERCENTAGE:
        lowRankFlag = True
    else:
        pass

    return lowRankFlag

refreshTime = time.time()
def fishFunc():
    global fishTimer
    global refreshTime
    global fishFlag

    if not fishFlag:
        return

    frameTime = 0.1
    sleepTime = 0.3

    # print(1/(time.time()-refreshTime), (time.time()-refreshTime))
    # refreshTime = time.time()

    image = cap.getFrame()

    if ignoreFlag:
        if getFishLevel(image[fishLevel[0]:fishLevel[1], fishLevel[2]:fishLevel[3]]):
            GPIO.output(DS4_LX[0], DS4_LX[2])
            time.sleep(sleepTime * 2)
            GPIO.output(DS4_LX[0], DS4_LX[1])

            fishTimer = threading.Timer(frameTime * 15, fishFunc)
            fishTimer.start()
            return

    if checkActive(image[activeR2[0]][activeR2[1]], activeR2):
        GPIO.output(DS4_R2[0], DS4_R2[2])
        time.sleep(sleepTime)
        GPIO.output(DS4_R2[0], DS4_R2[1])

    if checkActive(image[activeL2[0]][activeL2[1]], activeL2):
        GPIO.output(DS4_L2[0], DS4_L2[2])
        time.sleep(sleepTime)
        GPIO.output(DS4_L2[0], DS4_L2[1])

    if checkActive(image[activeUP[0]][activeUP[1]], activeUP):
        GPIO.output(DS4_UP[0], DS4_UP[2])
        time.sleep(sleepTime)
        GPIO.output(DS4_UP[0], DS4_UP[1])

    if getMainColor(image[activeSQUARE[0]:activeSQUARE[1], activeSQUARE[2]:activeSQUARE[3]]):
        # print('=======================> square')
        GPIO.output(DS4_SQUARE[0], DS4_SQUARE[2])
        GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[1])
        GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])
    elif getMainColor(image[activeTRIANGLE[0]:activeTRIANGLE[1], activeTRIANGLE[2]:activeTRIANGLE[3]]):
        # print('=======================> triangle')
        GPIO.output(DS4_SQUARE[0], DS4_SQUARE[1])
        GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[2])
        GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])
    elif getMainColor(image[activeCIRCLE[0]:activeCIRCLE[1], activeCIRCLE[2]:activeCIRCLE[3]]):
        # print('=======================> circle')
        GPIO.output(DS4_SQUARE[0], DS4_SQUARE[1])
        GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[1])
        GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[2])
    else:
        GPIO.output(DS4_SQUARE[0], DS4_SQUARE[1])
        GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[1])
        GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])

    fishTimer = threading.Timer(frameTime, fishFunc)
    fishTimer.start()

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
def pressR1():
    GPIO.output(DS4_R1[0], DS4_R1[2])
    time.sleep(1)
    GPIO.output(DS4_R1[0], DS4_R1[1])
    time.sleep(1)
def pressCap():
    # capture frame
    image = cap.getFrame()
    image = image[100:300, 150:500]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("temp.bmp", image)

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

def pressFish():
    global fishFlag
    global fishTimer
    if fishFlag:
        btnFish['bg'] = 'red'
        fishFlag = False
        fishTimer.cancel()
        time.sleep(2)
        GPIO.output(DS4_R2[0], DS4_R2[1])
        GPIO.output(DS4_L2[0], DS4_L2[1])
        GPIO.output(DS4_UP[0], DS4_UP[1])
        GPIO.output(DS4_SQUARE[0], DS4_SQUARE[1])
        GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[1])
        GPIO.output(DS4_CIRCLE[0], DS4_CIRCLE[1])
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
btnIgnore = tk.Button(root, text = 'keep', bg = 'red', height = btnHeight, width = btnWidth)
btnIgnore['command'] = pressIgnore
btnIgnore.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnFish = tk.Button(root, text = 'Fish', bg = 'red', height = btnHeight, width = btnWidth)
btnFish['command'] = pressFish
btnFish.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnR1 = tk.Button(root, text = 'R1', height = btnHeight, width = btnWidth)
btnR1['command'] = pressR1
btnR1.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnRowIndex = btnRowIndex + 1
btnColIndex = 0
btnQuit = tk.Button(root, text = 'QUIT', height = btnHeight, width = btnWidth, fg = 'red', command = handleClose)
btnQuit.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)


root.protocol("WM_DELETE_WINDOW", handleClose)

try:
    root.mainloop()
except KeyboardInterrupt:
    handleClose()