#!/usr/bin/python3

import tkinter as tk
import RPi.GPIO as GPIO
import threading
import time

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
slowFlag = True
attackTimer = 0
checkTimer = 0

# allow the camera to warmup
time.sleep(2)



refreshTime = time.time()
def attackFunc():
    global attackTimer
    global refreshTime
    global farmFlag
    global slowFlag

    if not farmFlag:
        return

    if slowFlag:
      attackTime = 3
    else:
      attackTime = 0.2

    sleepTime = 0.1
    attackTimer = threading.Timer(attackTime, attackFunc)
    attackTimer.start()

    # print(1/(time.time()-refreshTime), (time.time()-refreshTime))
    # refreshTime = time.time()

    GPIO.output(DS4_CROSS[0], DS4_CROSS[2])
    time.sleep(sleepTime)
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
def pressSlow():
    global slowFlag
    if slowFlag:
        btnSlow['bg'] = 'red'
        btnSlow['text'] = 'fast'
        slowFlag = False
    else:
        btnSlow['bg'] = 'green'
        btnSlow['text'] = 'slow'
        slowFlag = True

def handleClose():
    global attackTimer
    global checkTimer
    if attackTimer != 0:
        attackTimer.cancel()
    if checkTimer != 0:
        checkTimer.cancel()
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
btnSlow = tk.Button(root, text = 'slow', bg = 'green', height = btnHeight, width = btnWidth)
btnSlow['command'] = pressSlow
btnSlow.grid(row = btnRowIndex, column = btnColIndex, padx = btnPad, pady = btnPad)

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