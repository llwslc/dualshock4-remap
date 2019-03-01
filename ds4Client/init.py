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

cap = WebcamImageGetter()
cap.start()


def pressPS():
    GPIO.output(DS4_PS[0], DS4_PS[2])
    time.sleep(1)
    GPIO.output(DS4_PS[0], DS4_PS[1])
    time.sleep(1)
def pressA():
    GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[2])
    time.sleep(1)
    GPIO.output(DS4_TRIANGLE[0], DS4_TRIANGLE[1])
    time.sleep(1)
def pressB():
    GPIO.output(DS4_SQUARE[0], DS4_SQUARE[2])
    time.sleep(1)
    GPIO.output(DS4_SQUARE[0], DS4_SQUARE[1])
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

def pressUp():
    GPIO.output(DS4_UP[0], DS4_UP[2])
    time.sleep(1)
    GPIO.output(DS4_UP[0], DS4_UP[1])
    time.sleep(1)
def pressR1():
    GPIO.output(DS4_R1[0], DS4_R1[2])
    time.sleep(1)
    GPIO.output(DS4_R1[0], DS4_R1[1])
    time.sleep(1)
def pressR2():
    GPIO.output(DS4_R2[0], DS4_R2[2])
    time.sleep(1)
    GPIO.output(DS4_R2[0], DS4_R2[1])
    time.sleep(1)
def pressL1():
    GPIO.output(DS4_L1[0], DS4_L1[2])
    time.sleep(1)
    GPIO.output(DS4_L1[0], DS4_L1[1])
    time.sleep(1)
def pressL2():
    GPIO.output(DS4_L2[0], DS4_L2[2])
    time.sleep(1)
    GPIO.output(DS4_L2[0], DS4_L2[1])
    time.sleep(1)
def pressAccount():
    image = cap.getFrame()
    image = image[100:300, 150:500]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("account.bmp", image)
def pressCharacter():
    image = cap.getFrame()
    image = image[830:1030, 1470:1820]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("character.bmp", image)
def pressFish():
    image = cap.getFrame()
    image = image[949:967, 949:967]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("fish.bmp", image)
def pressIgnore():
    image = cap.getFrame()
    image = image[370:410, 1100:1300]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("ignoreItem.bmp", image)
def pressPickUp():
    image = cap.getFrame()
    image = image[440:470, 1100:1200]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("pickupItem.bmp", image)

def handleClose():
    cap.stop()
    root.destroy()
    GPIO.cleanup()


root = tk.Tk()
root.geometry('+0+0')

btnPS = tk.Button(root, text = 'PS', height = btnHeight, width = btnWidth)
btnPS['command'] = pressPS
btnPS.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnA = tk.Button(root, text = '△', height = btnHeight, width = btnWidth)
btnA['command'] = pressA
btnA.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnB = tk.Button(root, text = '口', height = btnHeight, width = btnWidth)
btnB['command'] = pressB
btnB.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

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
btnUp = tk.Button(root, text = 'Up', height = btnHeight, width = btnWidth)
btnUp['command'] = pressUp
btnUp.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnR1 = tk.Button(root, text = 'R1', height = btnHeight, width = btnWidth)
btnR1['command'] = pressR1
btnR1.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnR2 = tk.Button(root, text = 'R2', height = btnHeight, width = btnWidth)
btnR2['command'] = pressR2
btnR2.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnL1 = tk.Button(root, text = 'L1', height = btnHeight, width = btnWidth)
btnL1['command'] = pressL1
btnL1.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnL2 = tk.Button(root, text = 'L2', height = btnHeight, width = btnWidth)
btnL2['command'] = pressL2
btnL2.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)


btnRowIndex = btnRowIndex + 1
btnColIndex = 0
btnAccount = tk.Button(root, text = 'Account', height = btnHeight, width = btnWidth)
btnAccount['command'] = pressAccount
btnAccount.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnCharacter = tk.Button(root, text = 'Character', height = btnHeight, width = btnWidth)
btnCharacter['command'] = pressCharacter
btnCharacter.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnFish = tk.Button(root, text = 'Fish', height = btnHeight, width = btnWidth)
btnFish['command'] = pressFish
btnFish.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnIgnore = tk.Button(root, text = 'Ignore', height = btnHeight, width = btnWidth)
btnIgnore['command'] = pressIgnore
btnIgnore.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

btnColIndex = btnColIndex + 1
btnPickUp = tk.Button(root, text = 'PickUp', height = btnHeight, width = btnWidth)
btnPickUp['command'] = pressPickUp
btnPickUp.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)




root.protocol("WM_DELETE_WINDOW", handleClose)

try:
    root.mainloop()
except KeyboardInterrupt:
    handleClose()