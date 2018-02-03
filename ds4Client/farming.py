#!/usr/bin/python3

import tkinter as tk
import RPi.GPIO as GPIO
import threading
import time

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
farmTimer = 0
def farmFunc():
    global farmTimer
    farmTimer = threading.Timer(1, farmFunc)
    farmTimer.start()

    GPIO.output(DS4_L2, GPIO.HIGH)
    GPIO.output(DS4_CROSS, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(DS4_L2, GPIO.LOW)
    GPIO.output(DS4_CROSS, GPIO.LOW)

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
    global farmTimer
    if farmFlag:
        btnFarm['bg'] = 'red'
        farmFlag = False
        farmTimer.cancel()
        time.sleep(2)
        GPIO.output(DS4_L2, GPIO.HIGH)
        GPIO.output(DS4_CROSS, GPIO.HIGH)
    else:
        btnFarm['bg'] = 'green'
        farmFlag = True
        farmTimer = threading.Timer(1, farmFunc)
        farmTimer.start()

def handleClose():
    if farmTimer != 0:
        farmTimer.cancel()
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